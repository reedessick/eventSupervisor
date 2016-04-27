# Copyright (C) Reed Essick (2016)
#
# event_supervisor provides models for expected behavior from follow-up processes which annotate GraceDB. 
# the enclosed modules encapsulate the behavior of different processes and all are used within
# event_supervisor.py, which provides a "parseAlert" method which can be used with lvalert_listenMP
# This allows event_supervisor to dynamically update what needs to be monitored.
#
# The architecture is based off of the SortedQueue and QueueItem classes from ligo.lvalert.lvalertMPutils.py
# Each module defines new Item classes which inherit from QueueItem and are therefore safe to use within
# the SortedQueue.
