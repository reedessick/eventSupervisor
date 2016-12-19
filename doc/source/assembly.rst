==================================================
Assembly
==================================================

**eventSupervisor** contains (hard coded) logic about the workflow of expected follow-up. 
If process *A* annotates **GraceDb** with message *M*, and this triggers process *B* which should produce annotation *m*, the fact that annotation *M* should trigger a monitor of process *B* is encoded here. 

For more information about the exact workflow, see :doc:`architecture`.
We note that currently all dependencies are hard coded within the *new* and *parent_child* variables defined within *eventSupervisor.eventSupervisor.py*. 

eventSupervisor.eventSupervisor.py
--------------------------------------------------

.. automodule:: eventSupervisor.eventSupervisor
   :members:
