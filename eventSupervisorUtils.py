description = ""
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

from ligoMP.lvalert import lvalertMPutils as utils

import subprocess as sp

import traceback

import re

#---------------------------------------------------------------------------------------------------

### basic logging and email utilities

def writeGDBLog( gdb, graceid, message, tagnames=[] ):
    """
    writes a standard event_supervisor log message into gracedb
    """
    gdb.writeLog( graceid, message="ES:"+message, tagnames=['event_supervisor']+tagnames )

def emailWarning(subject, body, email):
    """
    issue an email to the addresses specified

    delegates to lvalertMPutils.sendEmail
    """
    utils.sendEmail( email, body, subject )

#---------------------------------------------------------------------------------------------------

### some basic look-up utilities

def isINJ( graceid, gdb, verbose=False ):
    """
    determines if the event is labeled as an injection
    """
    if verbose:
        print( "    looking up labels" )
    labels = gracedb.labels( gdb_id ).json()['labels']
    if verbose:
        if "INJ" in [label['name'] for label in labels]:
            report( "\tevent labeled \"INJ\"" )
            return True
        else:
            report( "\tevent not labeled \"INJ\"" )
            return False
    else:
        return "INJ" in [label['name'] for label in labels]

def filename2log( filename, logs, verbose=False ):
    """
    finds the log associated with a given filename
    """
    for log in logs[::-1]: ### iterate through logs in reverse so we get the most recent logs first
                           ### this means we will get the most recent version of files, if multiple exist
        if filename == log['filename']: ### this is the log message associated with that filename
            if verbose:
                print( "    %s assoicated with log message : %d"%(filename, log['N']) )
            return log
    else:
        raise ValueError( "could not find %s in association with any log messages"%(filename) )

def check4log( graceid, gdb, fragment, tagnames=None, verbose=False, regex=False ):
    """
    checks for the fragment in the logs for this graceid

    return action_required
    """
    if verbose:
        print( "    retrieving log messages" )
    logs = gdb.logs( graceid ).json()['log']

    if verbose:
        print( "    parsing log" )
    if regex:
        template = re.complile( fragment )
        for log in logs:
            comment = log['comment']
            if template.match( comment ):
                if tagnames!=None: ### check for tagnames
                    return sorted(log['tagnames']) != sorted(tagnames) ### log exists, so action_required depends only on tagnames
                else:
                    return False ### action_required = False (we found a match) 
        else:
            return True ### action_required = True (could not find a match)
    else:
        for log in logs:
            comment = log['comment']
            if fragment in comment:
                return False ### action_required = False (we found a match)
        else:
            return True ### action_required = True (could not find log)

def check4file( graceid, gdb, filename, regex=False, tagnames=None, verbose=False, logFragment=None, logRegex=False ):
    """
    checks for the existence of a file and that it is tagged correctly
    if tagnames==None, we ignore check for tagnames

    if regex, we interpret filename as a search string for regular expressions

    return warning, action_required
    """
    if verbose:
        print( "    retrieving filenames" )
    files = gdb.files( graceid ).json().keys()

    if regex:
        template = re.compile( filename )
        for f in files:
            if template.match( f ):
                file_exists = True
                filename = f
                break
        else:
            file_exists = False
    else:
        file_exists = filename in files

    if file_exists: ### file exists
        check_tagnames = tagnames!=None
        check_logFragment = logFragment!=None
        if (check_tagnames) or (check_logFrament):
            if verbose:
                print( "    retrieving log messages" )
            logs = gdb.logs( graceid ).json()['log']
            log = filename2log( fitsname, logs, verbose=verbose )

            if (check_tagnames) and (check_logFragment): ### check both tagnames and log message
                tagsGood = sorted(log['tagnames']) == sorted(tagnames)
                if logRegex:
                    template = re.compile( logFragment )
                    logGood = re.compile( logFragment ).match( log['comment'] )
                else:
                    logGood = logFragment in log['comment']

                if tagsGood and logGood:
                    warning = "found %s with correct tagnames (%s) and correct log message"%(filename, ",".join(tagnames))
                    return warning, False ### action_required = False
                elif tagsGood:
                    warning = "found %s with correct tagnames (%s) but incorrect log message"%(filename, ",".join(tagnames))
                    return warning, True ### action_required = True
                elif logGood:
                    warning = "found %s with correct log message but incorrect tagnames (%s)"%(filename, ",".join(log['tagnames']))
                    return warning, True ### action_required = True
                else:
                    warning = "found %s with incorrect tagnames (%s) and incorrect log message"%(filename, ",".join(log['tagnames']))
                    return warning, True ### action_required = True

            elif check_tagnames: ### check only tagnames
                if sorted(log['tagnames']) == sorted(tagnames): ### correct tags
                    warning = "found %s with correct tagnames (%s) while ignoring log message"%(filename, ",".join(tagnames))
                    return warning, False ### action_required = False
                else: ### wrong tagnames
                    warning = "found %s but with incorrect tagnames (%s) while ignoring log message"%(filename, ",".join(log['tagnames']))
                    return warning, True ### action_required = True

            else: ### check_logFragment -> check only log message
                if logRegex:
                    template = re.compile( logFragment )
                    logGood = re.compile( logFragment ).match( log['comment'] )
                else:
                    logGood = logFragment in log['comment']

                if logGood:
                    warning = "found %s with correct log message while ignoring tagnames"%(filename)
                    return warning, False ### action_required = False
                else:
                    warning = "found %s but with incorrect log message while ignoring tagnames"%(filename)
                    return warning, True ### action_required = True

        else: 
            warning = "found %s while ignoring tagnames and log message"%(fitsname)
            return warning, False ### action_required = False

    else: ### file does not exist
        warning = "could not find %s"%(fitsname)
        return warning, True ### action_required = True

#---------------------------------------------------------------------------------------------------

class EventSupervisorQueueItem(utils.QueueItem):
    """
    an object representing a sorted Queue to be used with event_supervisor
    items are sorted by their expiration times (when they timeout)

    WARNING: we may want to replace this with the SortedContainers module's SortedList(WithKey?) 
        almost certainly has faster insertion than what you've written and comes with many convenient features already implemented
    """
    name = "event supervisor item"
    description = "a series of connected tasks for event supervisor"

    def __init__(self, graceid, gdb, t0, tasks, annotate=False):
        self.graceid = graceid
        self.gdb = gdb
        self.annotate = annotate
        for task in tasks:
            if not isinstance(task, EventSupervisorTask):
                raise ValueError("each element of tasks must be an instance of eventSupervisorUtilts.EventSupervisorTask")
        super(EventSupervisorQueueItem, self).__init__(t0, tasks)

    def execute(self, verbose=False):
        """
        execute the next task
        """
        while len(self.tasks):
            self.expiration = self.tasks[0].expiration
            if self.hasExpired():
                task = self.tasks.pop(0) ### extract this task
                task.execute( self.graceid, self.gdb, verbose=verbose, annotate=self.annotate ) ### perform this task
                self.completedTasks.append( task ) ### mark as completed
            else:
                break
        self.complete = len(tasks)==0 ### only complete when there are no remaining tasks

class EventSupervisorTask(utils.Task):
    """
    a task to be completed by a QueueItem within event_supervisor
    this basic object manages execution via delegation to a functionHandle supplied when instantiated
    child classes may simply define their execution commands directly as part of the class definition
    """
    name = "event supervisor task"
    description = "a task for event supervisor"

    def __init__(self, timeout, functionHandle, email=[], *args, **kwargs ):
        self.email = email
        self.warning = None
        super(EventSupervisorTask, self).__init__(timeout, functionHandle, *args, **kwargs)

    def execute(self, graceid, gdb, verbose=False, annotate=False):
        """
        perform associated function call
        """
        try:
            if self.functionHandle( graceid, gdb, verbose=verbose, annotate=annotate, *self.args, **self.kwargs ):
                if self.email:
                    subject = "%s: %s requires attention"%(graceid, self.name)
                    url = "URL" ### extrace from gdb instance!
                    body = "%s: %s requires attention\n%s\nevent_supervisor found suspicous behavior when performing %s\n%s"%(graceid, name, url, self.description, self.warning)
                    emailWarning(subject, body, email=self.email)
        except Exception as e:
            if self.email:
                subject = "%s: %s FAILED"%(graceid, self.name)
                url = "URL" ### extrace from gdb instance!
                body = "%s: %s check FAILED\n%s\nevent_supervisor caught an exception when performing %s\n%s"%(graceid, name, url, description, traceback.format_exc())
                emailWarning(subject, body, email=self.email)
