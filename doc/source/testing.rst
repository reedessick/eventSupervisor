==================================================
Testing
==================================================

**eventSupervisor** provides 3 different types of testing, although there is no guarantee that these will cover all possible use cases.
Typically, the testing suite is called by hand when the developer is finished implementing a new monitor to make sure that the associated objects

    - are instantiated correctly base on a Config File (eventSupervisor_instantiationTests.py),
    - perform their actions as desired (eventSupervisor_executtionTests.py), and
    - are added to the *SortedQueue* correct based on *lvalert* messages (eventSupervisor_assemblyTests.py).

**Note**: these testing scripts are *not* installed as part of distribution with Grinch.

eventSupervisor_instantiationTests.py
--------------------------------------------------

This script ensures that *QueueItems* and *Tasks* are instantiated correctly and that their attributes are set to the appropriate values.
Several options allow the user to test different modules or broad classes of *QueueItems* such as ``--dq`` or ``--skymaps``.

**WRITE ME**
- basically copy the help string. Can we do this automatically?

eventSupervisor_executionTests.py
--------------------------------------------------

This script ensures that *QueueItems* and *Tasks* actually perform their actions as expected. 
It is the closest to a full-functionality test that is supported in these testing scripts. 
Several options allow the user to test different modules or broad classes of *QueueItems* such as ``--dq`` or ``--skymaps``.

**WRITE ME**
- basically copy the help string. Can we do this automatically?

eventSupervisor_assemblyTests.py
--------------------------------------------------

This script ensures that *QueueItems* are added to *queue* and *queueByGraceID* correctly by calling *parseAlert* with simulated input and a series of assertion statements on the output. 
It provides several command line options corresponding to different possible types of *lvalert* announcements and therefore different actions.

**WRITE ME**
- basically copy the help string. Can we do this automatically?
