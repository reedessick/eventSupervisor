# event_supervisor2
a holder for event_supervisor development based off the lvalertMP architecture

we divide each basic type of follow-up process into a separate package. Within each of these packages, modules define extensions of the lvalertMPutils.QueueItem class and all the required methods to support them. These are then used within event_supervisor.parseAlert in response to lvalert messages and are managed dynamically through an instance of ligo.lvalert.interactiveQueue.interactiveQueue running via multiprocessing from lvalert_listenMP.

All that being said, event_supervisor.parseAlert should contain the bulk of the logic associated with the project's goals and each package/module should really just provide a fall-back check which we peform by actually querying GraceDB (instead of just listening to lvalerts).

-------------------

eventSupervisor is organized into several different modules, each corresponding to a different type of follow-up activity. Within each module, extension of eventSupervisorUtils.EventSupervisorQueueItem (an extension of lvalertMPutils.QueueItem) and eventSupervisorUtils.EventSupervisorTask (an extension of lvalertMPutils.Task) are defined. These specify exactly what is expected of each follow-up process, how to check for it, and what action should be taken if deemed necessary. For the most part, this involves querying GraceDB for log messages and files. If they are missing or otherwise indicate a problem, an email is sent to the "responsible parties" but no other action is taken.

The QueueItems defines within each module have a standardized __init__() format, which extracts the required information directly from a config object. In this way, we can standardize how Items are created by passing the same arguments and simply iterating over the Item's names as specified in some directed graph. Furthermore, each QueueItem is responsible for defining the Tasks it needs within the Item's __init__() call. All defined items (subclass of eventSupervisorUtils.EventSupervisorQueueItem) are automatically identified from the modules loded in eventSupervisor.py. In this way, if we add a new Item or module, all that has to be updated is the "directed graph" which defines the parent/child relation ships (and possibly parsing to identify when new log messages satisfy checks).

Furthermore, the email formatting and error catching is handled automatically within EventSupervisorTask.execute() via delegation to a function handle stored as an attribute of the object.

-------------------

We also have a testing suite that checks that all objects are instantiated as expected. This includes both QueueItems and Tasks associated with all modules. Attributes are check via assertion statements but no actual functionality is tested.

The functionality (ie: Task.execute() methods) needs to be tested as well as the automatic redefinition of complete, completedTasks, tasks, and expiration attributes within QueueItem classes needs to be tested. Once this is shown to operate as expected, we can perform full-scale integration and functionality tests with lvalertMP via actual lvalert messages mimicing real GraceDB events.

-------------------

To Do:
  -- test Task.execute() and how attributes change accordingly.
  -- test Item.execute() and how attributes change (may only need to do this once because it is shared code)
  -- improve logging so that statements go into one big log as well as separate logs for each GraceID. 
  -- implement latency tools for Tasks: return how long after the event was created before the Task was completed.
  -- document new architecture, including flow charts showing inheritence and how parseAlert works. Be clear about how to add new Items/Tasks and what needs to be modified in parseAlert to support that.
  -- add ability to remove Items from the queue if alerts are received that render them unnecessary.
