==================================================
Logging
==================================================

How eventSupervisor structures its logs
--------------------------------------------------

**eventSupervisor** uses the standard Python Logging module and leverages the setup provided in **lvalertMP**.
This means that a copy of all log messages are reported to the logger generated within *interactiveQueue*.
What's more, the hierarchical structure of all logs are handled through the *logTag* kwarg passes to *QueueItems* and *Tasks* upon instantiation.
Furthermore, *EventSupervisorQueueItems* will automatically define a logger specifically for each *GraceID* separately, and will mirror the log messages into both loggers. 
These are written into the same directory as the main **lvalertMP** log by passing a *logDir* kwarg when *QueueItems* are instantiated.

Reading eventSupervisor logs
--------------------------------------------------

Because of the hierarchical structure of the loggers instantiated in *interactiveQueue* and wihtin **eventSupervisor**, reading the actual log messages should be rather straightforward. 
The log provides a time-stamp, a name corresponding to which bit of code is actually executing at that moment, a verbosity level and a message. 
The logger's name is built iteratively by appending *QueueItem* and *Task* objects' *name* attributes to the *logTag* kwargs they are given upon instantiation.
Delegation to utility functions are also denoted by deeper levels in the logger name. 

The loggers also print the full *Traceback* of any errors that are caught.
This, combined with the hierarchical structure of the logs, should greatly aid debugging because it naturally shows the workflow executed within the code.

In addition to local logs, **eventSupervisor** can annotate GraceDb.
Typically, there are restricted to only high level summary statements reporting the outcome of a check, are tagged "event_supervisor", and give a brief description of what was done and what conclusions were reached.
These are also posted verbatim into the local log files (entries with "action required" in the message).

Examples
~~~~~~~~~~~~~~~~~~~~~~~~~

lvalertMP log
+++++++++++++

Below is a verbatim example for a low significance cWB event form O2. 
This is what's printed to the full **lvalertMP** log

-    2016-12-15 08:45:13,876 | iQ : INFO : received : {"object": {"graceid": "G265912", "gpstime": "1165855145.5572", "pipeline": "CWB", "group": "Burst", "extra_attributes": {"MultiBurst": {"central_freq": "738.424011", "false_alarm_rate": null, "confidence": null, "start_time_ns": 531200000, "start_time": 1165855145, "ligo_angle_sig": null, "bandwidth": "182.672699", "snr": 10.14889156509222, "ligo_angle": null, "amplitude": "6.090949", "ligo_axis_ra": "61.672142", "duration": "0.010605", "ligo_axis_dec": "-32.442867", "peak_time_ns": null, "peak_time": null, "ifos": ""}}, "links": {"neighbors": "https://gracedb.ligo.org/api/events/G265912/neighbors/", "files": "https://gracedb.ligo.org/api/events/G265912/files/", "log": "https://gracedb.ligo.org/api/events/G265912/log/", "filemeta": "https://gracedb.ligo.org/api/events/G265912/filemeta/", "self": "https://gracedb.ligo.org/api/events/G265912", "labels": "https://gracedb.ligo.org/api/events/G265912/labels/", "emobservations": "https://gracedb.ligo.org/api/events/G265912/emobservation/", "tags": "https://gracedb.ligo.org/api/events/G265912/tag/"}, "created": "2016-12-15 16:45:13 UTC", "far": 3.79986e-06, "instruments": "H1,L1", "labels": {}, "search": "AllSky", "nevents": null, "submitter": "waveburst", "likelihood": 103, "far_is_upper_limit": false}, "alert_type": "new", "uid": "G265912", "file": "https://gracedb.ligo.org/events/G265912/files/trigger_1165855145.5572.txt", "description": ""}
-    2016-12-15 08:45:13,881 | iQ.parseAlert : DEBUG : added QueueItem=event creation
-    2016-12-15 08:45:13,881 | iQ.parseAlert : DEBUG : added QueueItem=far
-    2016-12-15 08:45:13,881 | iQ.parseAlert : DEBUG : added QueueItem=local rate
-    2016-12-15 08:45:13,882 | iQ.parseAlert : DEBUG : added QueueItem=creation rate
-    2016-12-15 08:45:13,882 | iQ.parseAlert : DEBUG : added QueueItem=external triggers
-    2016-12-15 08:45:13,882 | iQ.parseAlert : DEBUG : added QueueItem=unblind injections
-    2016-12-15 08:45:13,882 | iQ.parseAlert : DEBUG : added QueueItem=lldqReport
-    2016-12-15 08:45:13,882 | iQ.parseAlert : DEBUG : added QueueItem=idq start
-    2016-12-15 08:45:13,883 | iQ.parseAlert : DEBUG : added QueueItem=h1 omega scan start
-    2016-12-15 08:45:13,883 | iQ.parseAlert : DEBUG : added QueueItem=l1 omega scan start
-    2016-12-15 08:45:13,883 | iQ.parseAlert : DEBUG : added QueueItem=segdb2grcdb start
-    2016-12-15 08:45:13,883 | iQ.parseAlert : DEBUG : added QueueItem=notify
-    2016-12-15 08:45:13,883 | iQ.parseAlert : DEBUG : added QueueItem=cwb pe
-    2016-12-15 08:45:13,884 | iQ : INFO : performing : check sanity of reported FAR
-    2016-12-15 08:45:13,890 | iQ.far : DEBUG : executing far
-    2016-12-15 08:45:13,890 | iQ.far.far : DEBUG : executing far
-    2016-12-15 08:45:13,891 | iQ.far.far : INFO : G265912 : a check for propper FAR
-    2016-12-15 08:45:13,891 | iQ.far.far : DEBUG : retrieving event details
-    2016-12-15 08:45:15,124 | iQ.far.far : DEBUG : no action required : 0.000e+00 <= FAR=3.800e-06 <= 1.000e-03
-    2016-12-15 08:45:16,258 | iQ.far : DEBUG : far is complete

Note that this can become quite verbose quite quickly. 
The verbosity level can be controlled from the *lvalert_listenMP* Config File for the child processes via the *log_level* option.

GraceId-specific log
++++++++++++++++++++

We also provide some excerpt full log for the same event (G265912) from the log created specifically for that GraceId.
Note, the redundancy with the full log shown for the first check (*far*).

-    2016-12-15 08:45:13,890 | iQ.far : DEBUG : executing far
-    2016-12-15 08:45:13,890 | iQ.far.far : DEBUG : executing far
-    2016-12-15 08:45:13,891 | iQ.far.far : INFO : G265912 : a check for propper FAR
-    2016-12-15 08:45:13,891 | iQ.far.far : DEBUG : retrieving event details
-    2016-12-15 08:45:15,124 | iQ.far.far : DEBUG : no action required : 0.000e+00 <= FAR=3.800e-06 <= 1.000e-03
-    2016-12-15 08:45:16,258 | iQ.far : DEBUG : far is complete
-    2016-12-15 08:45:16,265 | iQ.local rate : DEBUG : executing local rate
-    2016-12-15 08:45:16,265 | iQ.local rate.localRate : DEBUG : executing localRate
-    2016-12-15 08:45:16,266 | iQ.local rate.localRate : INFO : G265912 : a module housing checks of basic event_supervisor functionality_AllSky
-    2016-12-15 08:45:16,266 | iQ.local rate.localRate : DEBUG : retrieving information about this event
-    2016-12-15 08:45:16,967 | iQ.local rate.localRate : DEBUG : gpstime : 1165855145.557200
-    2016-12-15 08:45:16,968 | iQ.local rate.localRate : DEBUG : retrieving neighbors within [1165855145.557200-10000.000000, 1165855145.557200+0.000000]
-    2016-12-15 08:45:17,993 | iQ.local rate.localRate : DEBUG : no action required : found 1 events within (-10000.000, +0.000) of G265912
-    2016-12-15 08:45:19,135 | iQ.local rate : DEBUG : local rate is complete
-    2016-12-15 08:45:21,924 | iQ.lldqReport : DEBUG : executing lldqReport
-    2016-12-15 08:45:21,927 | iQ.lldqReport.lldqReport : DEBUG : executing lldqReport
-    2016-12-15 08:45:21,927 | iQ.lldqReport.lldqReport : INFO : G265912 : a check that the lldq-report page was posted
-    2016-12-15 08:45:21,927 | iQ.lldqReport.lldqReport.check4log : DEBUG : retrieving log messages
-    2016-12-15 08:45:23,040 | iQ.lldqReport.lldqReport.check4log : DEBUG : parsing log
-    2016-12-15 08:45:23,040 | iQ.lldqReport.lldqReport : DEBUG :     no action required : found lldq-report post
-    2016-12-15 08:45:24,316 | iQ.lldqReport : DEBUG : lldqReport is complete
