==================================================
Architecture
==================================================

**eventSupervisor** is decomposed into a series of modules, each containing class declarations and methods for a particular type of follow-up.
Nonetheless, all these are treated on an equal footing at runtime and this structure is more organizational than functional.

Basic architecture within lvalertMP
--------------------------------------------------
The basic model is as follows:

    **lvalertMP** launches a child processes (via Python's multiprocessing package), which is an instance of *interactiveQueue*.
    This receives json strings from **lvalert** pubsub nodes and distributes them into the child processes through *multiprocessing.Connection* objects.
    It also iterates over a *SortedQueue* within a persistent loop, checking whether actions need to be performed by checking the *expiration* attribute of the first *QueueItem* in the *SortedQueue*. Because these are sorted, we are guaranteed that the first *QueueItem* in the list is the first one that needs attention.

    Each *QueueItem* has an *expiration* attribute, which encapsulates when it requires attention. 
    In this way, we can schedule something to happen some time in the future without blocking (i.e., avoiding *sleep* statements).
    *QueueItems* also posses an *execute* method, which is called when they expire.
    This delegates to a *Task* object (with a reference stored within the *QueueItem*), in which the actual ''work'' is done.

    Each *Task* object will either query **GraceDb** or otherwise perform some action to determine whether anyone needs to be alerted.
    If it deems action is required, it will alert a specified list of analysts via email.

Special Extensions unique to eventSupervisor
--------------------------------------------------

**eventSupervisor** defines a extensions to the standard **lvalertMP** *QueueItem* and *Task* objects.
These are called 

* EventSupervisorQueueItem
* EventSupervisorTask

EventSupervisorQueueItem
~~~~~~~~~~~~~~~~~~~~~~~~

biggest thing is that it stores some attributes that are passed to *EventSupervisorTask* upon execution because *interactiveQueue* does not pass all these (it only passes a *verbose* kwarg).

These extra attributes include

  - graceid
  - gdb (instance of ligo.gracedb.rest.GraceDb or equivalent)
  - warnings
  - annotate
  - logDir

It also ensures that all *Tasks* included in it are instances of *EventSupervisorTask*.
The *QueueItem* automatically handles logging via the *logDir* and *logTag* attributes, which are used upon calls to *execute* to retrieve the appropriate logger.

.. autoclass:: eventSupervisor.eventSupervisorUtils.EventSupervisorQueueItem

EventSupervisorTask
~~~~~~~~~~~~~~~~~~~

This is very similar to an *lvalertMP* *Task* except it provides special error handling and conditioning upon execution.
Delegation still occurs via *getattr(self, self.name)*, but upon execution *EventSupervisorTask* can alert one of 3 lists of analysis

  - emailOnSuccess
  - emailOnFailure
  - emailOnException

The Task also manages logging automatically upon calls to execute via *logDir* and *logTag* attributes. 

.. autoclass:: eventSupervisor.eventSupervisorUtils.EventSupervisorTask

Workflow within parseAlert
--------------------------------------------------

**lvalertMP**'s *interactiveQueue* calls *parseAlert* when a new *lvalert* announcement is received and invokes the following basic workflow:

1) *interactiveQueue* delegates to *eventSupervisor.eventSupervisor.parseAlert*
2) if needed, *parseAlert* delegates to *lvalertMP.lvalert.commands.parseCommand*, otherwise it builds a list of *QueueItems* that need to be added
    a) if *alert_type=new*, we simply iterate over the *names* in *new* and create *QueueItems* as necessary.
    b) if *alert_type=update*, we delegate to *parseUpdate* to determine what type of annotation it is. We then look up *names* in *parent_child* and create *QueueItems* as necessary.
    c) if *alert_type=label*, we do not add any *QueueItems*
    d) if *alert_type=signoff*, we do not add any *QueueItems*
    e) if *alert_type* is not recognized, we do not add any *QueueItems*
3) we iterate over the *QueueItems* that are to be added and instert them into *queue* and *queueByGraceID* as appropriate.

We note that instances of the *QueueItems* are first created and stored temporarily in an unsorted list, only to be added to *queue* and *queueByGraceID* later.
What's more, *QueueItems* are only actually created if the Config File has a section corresponding to the *QueueItem's* name.
*parseAlert* also supports basic thresholding on the False Alarm Rate (FAR) for *QueueItems* added when *alert_type=new*. 
If the Config File has a *far thr* option under the associated section, the *QueueItem* will be added if the event has a FAR associated with it and that FAR is smaller than *far thr*. 

*parseAlert* provides rather specific logging detailing each of these steps.
