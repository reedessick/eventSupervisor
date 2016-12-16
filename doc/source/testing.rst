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

**WRITE ME**

- basically copy the help string. Can we do this automatically?

eventSupervisor_executionTests.py
--------------------------------------------------

**WRITE ME**

- basically copy the help string. Can we do this automatically?

eventSupervisor_assemblyTests.py
--------------------------------------------------

**WRITE ME**

- basically copy the help string. Can we do this automatically?
