description = ""
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

from ligo.lvalert import lvalertMPutils as utils

import subprocess as sp

#---------------------------------------------------------------------------------------------------

def emailWarning(subject, body, email):
    """
    issue an email to the addresses specified
    """
    sp.Popen(["mail", "-s", subject, " ".join(email)], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE).communicate(body)

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
                    body = "%s: %s requires attention\n%s\nevent_supervisor found suspicous behavior when performing %s"%(graceid, name, url, description)
                    emailWarning(subject, body, email=self.email)
        except:
            if self.email:
                subject = "%s: %s FAILED"%(graceid, self.name)
                url = "URL" ### extrace from gdb instance!
                body = "%s: %s check FAILED\n%s\nevent_supervisor caught an exception when performing %s"%(graceid, name, url, description)
                emailWarning(subject, body, email=self.email)
