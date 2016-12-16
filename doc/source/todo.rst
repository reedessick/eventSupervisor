==================================================
To Do
==================================================

- add ability to remove *Items* from the queue if alerts are received that render them unnecessary (where lvalertMP becomes really useful).
  - we should give all *Tasks* a "satisfy" method or something which takes in a log message (or *lvalert* or something) and determines whether the *Task* is complete. This will be extremely useful when identifying which QueueItems are done as new alerts come in as well as obviating latency tools.
- implement latency tools for *Tasks*: return how long after the event was created before the Task was completed.
  - this will be helped by the giving all *Tasks* a "satisfy" method (will also be used to flag *Tasks* as complete within *parseAlert*)
- implement a more "fluid" way to denote the directed graph connecting the follow-up.
  - want to avoid the hard coded key:value pairs currently within eventSupervisor.py
  - want some sort of Parent:Child relationship with the edge length connecting the nodes to be the expected delay time
  - we then can have a "compiler" that takes the directed graph and writes the appropriate eventSupervisor config file
- remove *self.logDir* attributes from *EventSupervisorTask* objects (they no longer need it because *EventSupervisorQueueItems* create the *FileHandler*)
- generally clean up attributes saved under *QueueItems* and *Tasks* so that they are only stored if they are necessary. There's probably a decent amount of clutter right now.
