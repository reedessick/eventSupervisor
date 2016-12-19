==================================================
Monitors
==================================================

This serves as an exhaustive list of all *EventSupervisorQueueItems* and *EventSupervisorTasks* currently defined.
We note that the help-strings of each *QueueItem* describe how the attributes are set upon instantiation, specifying whether they are read from

  - the *lvalert* message (``alert``),
  - the Config File (``config``), or
  - from a query to GraceDb.

The help-strings of the *Tasks* briefly describe what is performed upon execution.
**CHANGE HELP-STRINGS WITHIN THE CODE TO MAKE THIS TRUE**

We do not enumerate the *name* attributes for the classes here, but as they serve mostly internal purposes that is seen as acceptable.
What's more, we note that while the *QueueItems* and *Tasks* are defined in different modules, they are all treated equally.
The structure of the source code is really just for book-keeping.

Some of these modules also contain methods (e.g., :func:`eventSupervisor.basic.basic.is_psd`). 
These are used within eventSupervisor.eventSupervisor.parseUpdate to identify *lvalert* messages as they are recieved.

notify
--------------------------------------------------

This provides basic notification when a new event is received.
Its scale is much smaller than the functionality supported within GraceDb itself and is mostly deprecated.
Nonetheless, it can provide a sanity check.

.. automodule:: eventSupervisor.notify.notify
   :members:

basic
--------------------------------------------------

This provides simple functionality common to all events.
This includes checking that all information expected during event creation was actually uploaded, the rate of candidates uploaded by a pipeline, and several other generic things.

.. automodule:: eventSupervisor.basic.basic
   :members:

approvalProcessor
--------------------------------------------------

**NOT IMPLEMENTED**

  - code exists, but it is not an accurate model of what ApprovalProcessor does.

dq
--------------------------------------------------

This checks for generic data quality posts, although this is currently restricted to whether the low-latency data quality (lldq) report was posted.

.. automodule:: eventSupervisor.dq.dq
   :members:

idq
--------------------------------------------------

This checks that iDQ both started and uploaded all information for both sites. 
We explicitly look for all information that the pipeline uploads, including PNG figures and the JSON files they respresent.

.. automodule:: eventSupervisor.dq.idq
   :members:

segDB2grcDB
--------------------------------------------------

This checks for the existence of ligolw segment xml tables through predictable filenames.

.. automodule:: eventSupervisor.dq.segDB2grcDB
   :members:

omegaScan
--------------------------------------------------

This checks for links to automated OmegaScans as well as corresponding JSON files which store static URLs to the actual images.

.. automodule:: eventSupervisor.dq.omegaScan
   :members:

skymaps
--------------------------------------------------

This contains checks of any FITS file uploaded to GraceDb.
It checks for normalization as well as some generic follow-up that's expected.
Specifically,

  - plotting all skymaps on a mollweide projection in Equatorial coordinates
  - the appropriate JSON file created by skyviewer for further visualization of the skymap.

.. automodule:: eventSupervisor.skymaps.skymaps
   :members:

skymapSummary
--------------------------------------------------

This checks the automatec skymap summary and comparison was carried out.

.. automodule:: eventSupervisor.skymaps.skymapSummary
   :members:

embright
--------------------------------------------------

This looks for the results of EM Bright classification.
Currently, this monitor is very simple and could be expanded in the future.

.. automodule:: eventSupervisor.pe.embright
   :members:

bayestar
--------------------------------------------------

Checks that Bayestar started and reported a skymap.

.. automodule:: eventSupervisor.pe.bayestar
   :members:

bayeswavePE
--------------------------------------------------

Checks that BayesWave parameter estimation started and that it reported the expected results.

.. automodule:: eventSupervisor.pe.bayeswavePE
   :members:

cwbPE
--------------------------------------------------

Checks that cWB parameter estimation reported the expected results.

.. automodule:: eventSupervisor.pe.cwbPE
   :members:

lalinf
--------------------------------------------------

Checks that LALInference parameter estimation started and reported the expected results.

.. automodule:: eventSupervisor.pe.lalinf
   :members:

libPE
--------------------------------------------------

Checks that LIB parameter estimation started and reported the expected results.

.. automodule:: eventSupervisor.pe.libPE
   :members:
