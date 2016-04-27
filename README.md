# event_supervisor2
a holder for event_supervisor development based off the lvalertMP architecture

we divide each basic type of follow-up process into a separate package. Within each of these packages, modules define extensions of the lvalertMPutils.QueueItem class and all the required methods to support them. These are then used within event_supervisor.parseAlert in response to lvalert messages and are managed dynamically through an instance of ligo.lvalert.interactiveQueue.interactiveQueue running via multiprocessing from lvalert_listenMP.

All that being said, event_supervisor.parseAlert should contain the bulk of the logic associated with the project's goals and each package/module should really just provide a fall-back check which we peform by actually querying GraceDB (instead of just listening to lvalerts).
