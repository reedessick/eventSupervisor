==================================================
Introduction
==================================================

**eventSupervisor** monitors asynchronous distributed processes that upload information to GraceDb.
It is meant to be run on a single machine and integrated with **lvalertMP** to receive announcements
from **GraceDb**.
In this way, we can monitor an arbitrary number of processes without actually knowing where or how 
they run, but simply validating their output.

It is distributed as part of the Grinch library and most use cases will require only a single 
instance of *lvalert_listenMP* to exist.
This is because *lvalert* announcements from any particular pubsub node will only need to be fed 
into a single **eventSupervisor** child process.

Statement of the Problem
--------------------------------------------------

When gravitational wave candidates are uploaded to GraceDb, they trigger a wide range of automated 
follow-up. 
This includes

  - data quality information,
  - parameter estimation, and
  - human responses.

What's more, the automated follow-up can trigger more automated follow-up.
A good example of this is localization (skymaps).
When a skymap if uploaded, several automated processes are triggered to summarize and plot it.
Indeed, one can concoct an arbitrarily complicated workflow using GraceDb annotations to trigger 
processes.
This workflow can be arbitrarily distributed across many machines, and therefore monitoring the 
success or failure of these processes is only really tractable by monitoring their annotations 
within GraceDb.

Note, we cannot use Nagios to monitor most processes because the actual number of processes is
dynamic and changes in response to annotations within **GraceDb**.
Generally, *Nagios* *is* used to monitor the *lvalert_listen* instances which launch follow-up
processes.
Nonetheless, it has been observed that *lvalert_listen* can hang or otherwise persist while
the actual processes' functionality fails.
This means that *Nagios* may believe the process is in a nominal state when it actually fails
to annotate GraceDb.
**eventSupervisor** guarantees the processes are actually working because it monitors annotations
in **GraceDb** directly.

Methodology of Solution
--------------------------------------------------

The most basic summary of **eventSupervisor**'s solution is to 

    monitor follow-up processes by checking annotations in **GraceDb** for expected output on a 
    pre-determined time scale, sending warning messages if the expected behavior is not 
    observed.

It accomplishes this through a combination of queries to **GraceDb** and parsing annotation 
announcements distributed through *LVAlert*.
Specifically, **eventSupervisor** can be run under **lvalertMP**. 

Connection to lvalertMP
~~~~~~~~~~~~~~~~~~~~~~~~~

**WRITE ME!**
Describe how this is structured via *SortedQueue*, *QueueItem*, and *Task* objects.

Integration with Config File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**WRITE ME!**
Focus on how important the *name* attribute is.

Differences relative to O1
--------------------------------------------------

**WRITE ME**
A single process that handles multiple events and processes multiple *lvalert* announcments instead of one process per event that only ingests information from *alert_type=new* announcements.
Note, we could have used an architecture based on *lvalert_listen* to enable responses to *alert_type=update* annoncments as well.
The main advantage of *lvalertMP* is that it allows us to ingest information from new alerts within the same process and therefore can reduce the number of queries made to GraceDb. 
Again, this could have been done via *lvalert_listen*, but processes would likely have had to communicate through the filesystem.
*lvalertMP* allows us to handle everything in memory and forces execution to be serial, which can simplify or remove some race condistions associated with asynchronous processes communicating through the filesystem.
