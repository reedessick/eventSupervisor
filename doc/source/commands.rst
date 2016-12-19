==================================================
Commands
==================================================

**eventSupervisor** supports the standard **lvalertMP** commands and delegates to *parseCommand* within *parseAlert*.
It does not define any commands for this library alone.

As currently configured (see :doc:`production`), each child process has a separate command pubsub node.
These are owned by the ``gracedb.processor`` *lvalert* account and therefore commands must be sent with those credentials. 
