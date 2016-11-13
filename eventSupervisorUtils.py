description = "a module containing utility methods and class declarations"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

from lvalertMP.lvalert import lvalertMPutils as utils
from lvalertMP.lvalert.lvalertMPutils import genLogname
from lvalertMP.lvalert.lvalertMPutils import genFormatter

import logging

import subprocess as sp

import traceback

import re

#---------------------------------------------------------------------------------------------------

def genItemLogger( directory, name, logTag='iQ', graceid=None ):
    """
    returns a logger set up for QueueItems

    if a graceid is supplied, we also set up a FileHandler for that log specifically
    """
    logger = logging.getLogger('%s.%s'%(logTag, name))

    if graceid: ### specify the graceid logger specifically
        logname = genLogname(directory, graceid)

        for handler in logger.handlers: ### ensure it doesn't already exist to avoid repeated log statements
            if isinstance(handler, logging.FileHandler) and handler.baseFilename==logname:
                break

        else: ### handler doesn't exist, so we add it
            handler = logging.FileHandler( logname )
            handler.setFormatter( genFormatter() )
            logger.addHandler( handler )

    return logger

def genTaskLogger( directory, name, logTag='iQ' ):
    """
    returns a logger set up for Tasks
    """
    return logging.getLogger('%s.%s'%(logTag, name))

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

def isINJ( graceid, gdb, verbose=False, logTag='iQ' ):
    """
    determines if the event is labeled as an injection
    """
    if verbose:
        logger = logging.getLogger('%s.isINJ'%logTag) ### inheritance of loggers controlled by kwarg
        logger.debug( "looking up labels" )
    labels = gdb.labels( graceid ).json()['labels']

    if verbose:
        if "INJ" in [label['name'] for label in labels]:
            logger.debug( "event labeled \"INJ\"" )
            return True

        else:
            logger.debug( "event not labeled \"INJ\"" )
            return False

    else:
        return "INJ" in [label['name'] for label in labels]

def filename2log( filename, logs, verbose=False, logTag='iQ' ):
    """
    finds the log associated with a given filename
    """
    for log in logs[::-1]: ### iterate through logs in reverse so we get the most recent logs first
                           ### this means we will get the most recent version of files, if multiple exist
        if filename == log['filename']: ### this is the log message associated with that filename
            if verbose:
                logger = logging.getLogger('%s.filename2log'%logTag) ### inheritance of loggers controlled by kwarg
                logger.debug( "%s assoicated with log message : %d"%(filename, log['N']) )
            return log
    else:
        raise ValueError( "could not find %s in association with any log messages"%(filename) )

def check4log( graceid, gdb, fragment, tagnames=None, regex=False, verbose=False, logTag='iQ' ):
    """
    checks for the fragment in the logs for this graceid

    return action_required
    """
    if verbose:
        logger = logging.getLogger('%s.check4log'%logTag)
        logger.debug( "retrieving log messages" )
    logs = gdb.logs( graceid ).json()['log']

    if verbose:
        logger.debug( "parsing log" )

    if regex: ### use regular expressions
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

    else: ### use basic string parsing
        for log in logs:
            comment = log['comment']
            if fragment in comment:
                return False ### action_required = False (we found a match)

        else:
            return True ### action_required = True (could not find log)

def check4file( graceid, gdb, filename, regex=False, tagnames=None, logFragment=None, logRegex=False, verbose=False, logTag='iQ' ):
    """
    checks for the existence of a file and that it is tagged correctly
    if tagnames==None, we ignore check for tagnames

    if regex, we interpret filename as a search string for regular expressions

    return warning, action_required
    """
    if verbose:
        logger = logging.getLogger('%s.check4file'%logTag)
        logger.debug( "    retrieving filenames" )
    files = gdb.files( graceid ).json().keys()

    if regex: ### use regular expressions
        template = re.compile( filename )
        for f in files:
            if template.match( f ):
                file_exists = True
                filename = f
                break

        else:
            file_exists = False

    else: ### use basic string matching
        file_exists = filename in files

    if file_exists: ### file exists
        check_tagnames = tagnames!=None
        check_logFragment = logFragment!=None

        if (check_tagnames) or (check_logFrament):
            if verbose:
                logger.debug( "retrieving log messages" )
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

    def __init__(self, graceid, gdb, t0, tasks, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        self.graceid = graceid
        self.gdb = gdb

        self.warnings = warnings
        self.annotate = annotate

        self.logDir = logDir

        for task in tasks:
            if not isinstance(task, EventSupervisorTask):
                raise ValueError("each element of tasks must be an instance of eventSupervisorUtilts.EventSupervisorTask")

        super(EventSupervisorQueueItem, self).__init__(t0, tasks, logTag=logTag)

    def execute(self, verbose=False):
        """
        execute the next task

        NOTE: we overwrite the parent's method here because of the different signature for EventSupervisorTask.execute

        editing the correct file!
        """
        if verbose:
            logger = genItemLogger( self.logDir, self.name, logTag=self.logTag, graceid=self.graceid )
            logger.debug( 'executing %s'%self.name )

        while len(self.tasks):
            self.expiration = self.tasks[0].expiration
            if self.hasExpired():
                task = self.tasks.pop(0) ### extract this task
                task.execute( self.graceid, self.gdb, verbose=verbose, annotate=self.annotate, warnings=self.warnings ) ### perform this task
                ### NOTE: this next step could introduce a race condition, althouth it is unlikely to ever actually matter
                ###   a more proper solution would be to give task objects "complete" attributes and to check that, but
                ###   this should work well enough
                if task.hasExpired(): ### check whether task is actually done
                    self.completedTasks.append( task ) ### mark as completed

                else:
                    self.add( task )

            else:
                break

        self.complete = len(self.tasks)==0 ### only complete when there are no remaining tasks
        if verbose:
            if self.complete:
                logger.debug( '%s is complete'%self.name )
            else:
                logger.debug( '%s is NOT complete'%self.name )

class EventSupervisorTask(utils.Task):
    """
    a task to be completed by a QueueItem within event_supervisor
    this basic object manages execution via delegation to a functionHandle supplied when instantiated
    child classes may simply define their execution commands directly as part of the class definition
    """
    name = "eventSupervisorTask"
    description = "a task for event supervisor"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ', **kwargs ):
        self.email = email
        self.warning = None
        self.logDir = logDir

        super(EventSupervisorTask, self).__init__(timeout, logTag=logTag, **kwargs)

    def execute(self, graceid, gdb, verbose=False, annotate=False, warnings=False):
        """
        perform associated function call
        """
        if verbose:
            logger = genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.debug( 'executing %s'%self.name )

        try:
            if getattr(self, self.name)( graceid, gdb, verbose=verbose, annotate=annotate, **self.kwargs ):
                if warnings and self.email:
                    subject = "%s: %s requires attention"%(graceid, self.name)
                    url = gdb.service_url
                    body = "%s: %s requires attention\n%s\nevent_supervisor found suspicous behavior when performing %s\nwarning : %s"%(graceid, self.name, url, self.description, self.warning)
                    emailWarning(subject, body, email=self.email)
        
        except Exception as e:
            if verbose:
                logger.warn( '%s raise an exception!'%self.name )

            if warnings and self.email:
                subject = "%s: %s FAILED"%(graceid, self.name)
                url = gdb.service_url 
                body = "%s: %s check FAILED\n%s\nevent_supervisor caught an exception when performing %s\n%s"%(graceid, self.name, url, self.description, traceback.format_exc())
                emailWarning(subject, body, email=self.email)

    def eventSupervisorTask(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        '''
        required for syntactic completion of this class
        '''
        pass
