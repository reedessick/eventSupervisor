description = ""
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

from ligo.lvalert import lvalertMPutils as utils

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
    """
    sp.Popen(["mail", "-s", subject, " ".join(email)], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE).communicate(body)

#---------------------------------------------------------------------------------------------------

### some basic look-up utilities

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

def check4log( graceid, gdb, fragment, verbose=False ):
    """
    checks for the fragment in the logs for this graceid

    return action_required
    """
    if verbose:
        print( "    retrieving log messages" )
    logs = gdb.logs( graceid ).json()['log']

    if verbose:
        print( "    parsing log" )
    for log in logs:
        comment = log['comment']
        return fragment in comment

    return True ### action_required = True

def check4file( graceid, gdb, filename, tagnames=None, verbose=False, regex=False ):
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
        if tagnames!=None:
            if verbose:
                print( "    retrieving log messages" )
            logs = gdb.logs( graceid ).json()['log']
            log = filename2log( fitsname, logs, verbose=verbose )

            if sorted(log['tagnames']) == sorted(tagnames): ### correct tagnames
                warning = "found %s with correct tagnames (%s)"%(fitsname, ",".join(self.tagnames))
                return warning, False ### action_required = False
    
            else: ### wrong tagnames
                warning = "found %s but with incorrect tagnames (%s)"%(fitsname, ",".join(log['tagnames']))
                return warning, True ### action_required = True

        else: 
            warning = "found %s and ignoring tagnames"%(fitsname)
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

    def __init__(self, graceid, gdb, t0, tasks, description="a series of connected tasks", annotate=False):
        self.graceid = graceid
        self.gdb = gdb
        self.annotate = annotate
        for task in tasks:
            if not isinstance(task, EventSupervisorTask):
                raise ValueError("each element of tasks must be an instance of eventSupervisorUtilts.EventSupervisorTask")
        super(EventSupervisorQueueItem, self).__init__(t0, tasks, description=description)

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

    def __init__(self, timeout, functionHandle, name="task", description="a task", email=[], *args, **kwargs ):
        self.email = email
        self.warning = None
        super(EventSupervisorTask, self).__init__(timeout, functionHandle, name=name, description=description, *args, **kwargs)

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
