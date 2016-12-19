==================================================
Production Configurations
==================================================

production configuration files are stored within the repository itself for reference and are installed by Grinch via *setup.py*.

O1
--------------------------------------------------

This config is **not** stored within the respository. 
The code is deprecated and this should not be an issue.

ER10
--------------------------------------------------

These live within *etc* within the repository, with a corresponding *ER10-* prefix.

O2a
--------------------------------------------------

These are the currently used config files. 
They also live within *etc* within the repository and possess a *O2-* prefix.
Briefly, **eventSupervisor** is configured to divide messages into the following child processes based on who needs to be contacted for each.
Note, the command nodes are owned by the ``gracedb.processor`` *lvalert* account (see :doc:`commands`).

- pycbc

  - cbc_pycbc
  - command-eventSupervisor_pycbc

- gstlal

  - cbc_gstlal_lowmass
  - cbc_gstlal_highmass
  - command-eventSupervisor_gstlal

- gstlal-spiir

  - cbc_gstlal-spiir
  - command-eventSupervisor_gstlal-spiir

- mbta

  - cbc_mbtaonline
  - command-eventSupervisor_mbtaonline

- cwb

  - burst_cwb_allsky
  - command-eventSupervisor_cWB

- cwb long

  - burst_cwb_allskylong
  - command-eventSupervisor-cWBLong

- olib

  - burst_lib
  - command-eventSupervisor_oLIB

- external

  - external_swift
  - external_fermi
  - external_snews
  - command-eventSupervisor_External
