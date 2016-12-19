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

    if a graceid is supplied, we also set up a FileHandler for that log specifically.
    directory is only used if we set up a FileHandler for the graceid. 
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
    NOTE: directory is not used!
    """
    return logging.getLogger('%s.%s'%(logTag, name))

#---------------------------------------------------------------------------------------------------

### basic logging and email utilities

def writeGDBLog( gdb, graceid, message, tagnames=[] ):
    """
    writes a standard event_supervisor log message into gracedb
    ensures the annotation is tagged "event_supervisor"
    """
    gdb.writeLog( graceid, message="ES: "+message, tagname=['event_supervisor']+tagnames )

def emailWarning(subject, body, email):
    """
    issue an email to the addresses specified
    delegates to lvalertMPutils.sendEmail, which in turn delegates to the OS's mailx command
    """
    utils.sendEmail( email, body, subject )

def gdb2url( gdb, graceid):
    """
    generates a link to the gracedb page for graceid.
    used when generationg email warnings about specific events.
    """
    return "%s/events/view/%s"%(gdb.service_url.strip('api/'), graceid)

#---------------------------------------------------------------------------------------------------

### some basic look-up utilities

def isINJ( graceid, gdb, verbose=False, logTag='iQ' ):
    """
    determines if the event is labeled as an injection.
    Queries GraceDb for labels associated for this event and looks for an exact match for "INJ"

    return True if labeled INJ else False
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

    return log or raise ValueError if no log is found
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
    Queries GraceDb for log messages.

    if tagnames!=None, we require tagnames to exactly match those of the log. 
    if regex, we look for a regular expression match of the log comment with fragment instead of just "fragment in comment"

    return False if found log else True
    """
    if verbose:
        logger = logging.getLogger('%s.check4log'%logTag)
        logger.debug( "retrieving log messages" )
    logs = gdb.logs( graceid ).json()['log']

    if verbose:
        logger.debug( "parsing log" )

    if regex: ### use regular expressions
        template = re.compile( fragment )
        for log in logs:
            comment = log['comment']
            if template.match( comment ):
                if tagnames!=None: ### check for tagnames
                    return sorted(log['tag_names']) != sorted(tagnames) ### log exists, so action_required depends only on tagnames

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
    if logFragment!=None, we look for a match to the log comment as well
    if logRegex, we use regular expressions when matching the log comment.

    constructs a warning message describing the results of the query.
    action_required is True if anything is not correct and False only if all parts of the query pass.

    return warning, action_required
    """
    if verbose:
        logger = logging.getLogger('%s.check4file'%logTag)
        logger.debug( "retrieving filenames" )
    files = gdb.files( graceid ).json().keys()

    if regex: ### use regular expressions
        template = re.compile( filename )
        for f in files:
            if template.match( f ):
                file_exists = True

                ### WARNING: we strip the suffix GraceDb appends to filenames if it is present. 
                ###          This may break things if we're looking for a file with that suffix, but that's not the expected use case...
                f = f.split(',')[0]

                filename = f
                break

        else:
            file_exists = False

    else: ### use basic string matching
        file_exists = filename in files

    if file_exists: ### file exists
        check_tagnames = tagnames!=None
        check_logFragment = logFragment!=None

        if (check_tagnames) or (check_logFragment):
            if verbose:
                logger.debug( "retrieving log messages" )
            logs = gdb.logs( graceid ).json()['log']
            log = filename2log( filename, logs, verbose=verbose )

            if (check_tagnames) and (check_logFragment): ### check both tagnames and log message
                tagsGood = sorted(log['tag_names']) == sorted(tagnames)
                if logRegex:
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
                if sorted(log['tag_names']) == sorted(tagnames): ### correct tags
                    warning = "found %s with correct tagnames (%s) while ignoring log message"%(filename, ",".join(tagnames))
                    return warning, False ### action_required = False

                else: ### wrong tagnames
                    warning = "found %s but with incorrect tagnames (%s) while ignoring log message"%(filename, ",".join(log['tag_names']))
                    return warning, True ### action_required = True

            else: ### check_logFragment -> check only log message
                if logRegex:
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
            warning = "found %s while ignoring tagnames and log message"%(filename)
            return warning, False ### action_required = False

    else: ### file does not exist
        warning = "could not find %s"%(filename)
        return warning, True ### action_required = True

#---------------------------------------------------------------------------------------------------

class EventSupervisorQueueItem(utils.QueueItem):
    """
    an object representing a single follow up processes used with eventSupervisor
    The basic idea is to group a list of Tasks within a QueueItem, with each Task corresponding to an individual bit of information that should be checked.

    requires the following arguments upon instantiation
        - graceid  (the GraceId of the event this QueueItem will monitor)
        - gdb      (an instance of ligo.gracedb.rest.GraceDb or equivalent)
        - t0       (the time relative to which the expiration time is set. Passed to parent's __init__ to set Task expirations)
        - tasks    (a list of EventSupervisorTasks. Does not have to be ordered)
        - annotate (determines whether GraceDb is annotated when tasks are executed)
        - warnings (determines whether email warnings are sent when tasks are executed)
        - logDir   (used when instantiating a logger)
        - logTag   (used when instantiating a logger)
     
    This is an extension of lvalertMPutils.QueueItem with special attributes defined for eventSupervisor. 
    In particular, upon execution we call the Tasks with signature
        task.execute( 
            self.graceid, 
            self.gdb, 
            verbose=verbose, 
            annotate=self.annotate, 
            warnings=self.warnings
        )
    where the attributes are stored at instatiation time. 

    We note that sorting and handling Tasks is accomplished within lvalertMPutils.QueueItem and we simply delegate to that functionality.
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
        execute Tasks until all are complete or the remaining Tasks have not yet expired.
        NOTE: we overwrite the parent's method here because of the different signature for EventSupervisorTask.execute
        """
        if verbose:
            logger = genItemLogger( self.logDir, self.name, logTag=self.logTag, graceid=self.graceid )
            logger.debug( 'executing %s'%self.name )

        while len(self.tasks):
            self.expiration = self.tasks[0].expiration
            if self.hasExpired():
                task = self.tasks.pop(0) ### extract this task
                task.execute( 
                    self.graceid, 
                    self.gdb, 
                    verbose=verbose, 
                    annotate=self.annotate, 
                    warnings=self.warnings,
                ) ### perform this task
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
    a task to be completed by an EventSupervisorQueueItem
    this basic object manages execution via delegation to a method discoverable via
        getattr(self, self.name)
    While this is a bit of a backflip, it allows us to standardize the execution of each Task with a single function decleared here, rather than repeating code in each extension of this class.
    Furthermore, by storing the actual execution code under a method accessible through getattr instead of a function handle, we allow Python to pickle these objects (function handles are not resolvable when pickling).

    child classes may simply define their execution commands directly as part of the class definition, but this will overwrite the email and warning handling defined herein.
    This basic class defines

        - timeout          (the amount of time to wait before performing this Task)
        - emailOnSuccess   (the list of email addresses to notify if the check completed successfully and did not find anything wrong)
        - emailOnFailure   (the list of email addresses to notify if the check completed successfully and found suspicious behavior)
        - emailOnException (the list of email addresses to notify if the check did not copmlete successfully)
        - logDir           (directory into which loggers will be written. Passed to genTaskLogger in which it is not used...)
        - logTag           (used to define the hierarchical logger names)

    and captures any other arguments with **kwargs
    """
    name = "eventSupervisorTask"
    description = "a task for event supervisor"

    def __init__(self, timeout, emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ', **kwargs ):
        self.emailOnSuccess = emailOnSuccess
        self.emailOnFailure = emailOnFailure
        self.emailOnException = emailOnException

        self.warning = None
        self.logDir = logDir

        super(EventSupervisorTask, self).__init__(timeout, logTag=logTag, **kwargs)

    def execute(self, graceid, gdb, verbose=False, annotate=False, warnings=False):
        """
        perform associated function call by looking up a method via
            getattr(self, self.name)( graceid, gdb, verbose=verbose, annotate=annotate, **self.kwargs )

        if self.warnings and the appropriate email list is non-empty, constructs and sends email messages describing the check
        """
        if verbose:
            logger = genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.debug( 'executing %s'%self.name )

        try:
            if getattr(self, self.name)( graceid, gdb, verbose=verbose, annotate=annotate, **self.kwargs ):
                if warnings and self.emailOnFailure:
                    subject = "%s: %s requires attention"%(graceid, self.name)
                    url = gdb2url( gdb, graceid )
                    body = "%s: %s requires attention\n%s\nevent_supervisor found suspicous behavior when performing %s\nwarning : %s"\
                               %(graceid, self.name, url, self.description, self.warning)
                    emailWarning(subject, body, email=self.emailOnFailure)

            else:
                if warnings and self.emailOnSuccess:
                    subject = "%s: %s succeeded"%(graceid, self.name)
                    url = gdb2url( gdb, graceid )
                    body = "%s: %s succeeded\n%s\nevent_supervisor found only expected behavior when performing %s\nnotes : %s"\
                               %(graceid, self.name, url, self.description, self.warning)
                    emailWarning(subject, body, email=self.emailOnSuccess)
        
        except Exception as e:
            trcbk = traceback.format_exc().strip("\n")
            if verbose:
                logger.warn( '%s raised an exception!'%self.name )
                logger.warn( trcbk )

            if warnings and self.emailOnException:
                subject = "%s: %s FAILED"%(graceid, self.name)
                url = gdb2url( gdb, graceid )
                body = "%s: %s check FAILED\n%s\nevent_supervisor caught an exception when performing %s\n%s"\
                           %(graceid, self.name, url, self.description, trcbk)
                emailWarning(subject, body, email=self.emailOnException)

    def eventSupervisorTask(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        '''
        required for syntactic completion of this class.
        Currently just returns False
        '''
        return False
