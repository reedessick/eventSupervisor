description = "a module housing checks of basic functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

from ligo.lvalert import lvalertMPutils as utils

#---------------------------------------------------------------------------------------------------

#------------------------
# EventCreation
#------------------------

class EventCreationItem(utils.QueueItem):
    """
    a check for propper event creation and readability of associated trigger files
    """

    def __init__(self, graceid, gdb, pipeline, t0, timeout, gdb=None, verbose=False):
        description = "check %s event creation and trigger files"%(pipeline)
        if pipeline=="cwb":
            super(EventCreation, self).__init__(graceid, t0, timeout, cwbEventCreation, description=description, gdb=gdb, verbose=verbose)
        elif pipeline=="lib":
            super(EventCreation, self).__init__(graceid, t0, timeout, olibEventCreation, description=description, gdb=gdb, verbose=verbose)
        elif pipeline=="gstlal":
            super(EventCreation, self).__init__(graceid, t0, timeout, gstlalEventCreation, description=description, gdb=gdb, verbose=verbose)
        elif pipeline=="mbtaonline":
            super(EventCreation, self).__init__(graceid, t0, timeout, mbtaEventCreation, description=description, gdb=gdb, verbose=verbose)
        elif pipeline=="gstlal-spiir":
            super(EventCreation, self).__init__(graceid, t0, timeout, spiirEventCreation, description=description, gdb=gdb, verbose=verbose)
        elif pipeline=="pycbc":
            super(EventCreation, self).__init__(graceid, t0, timeout, pycbcEventCreation, description=description, gdb=gdb, verbose=verbose)
        else:
            raise ValueError("pipeline=%s not understood"%pipeline)

###
def cwbEventCreation( graceid, gdb=None, verbose=False ):
    """
    event creation sanity check for cWB
    we check:
        trigger.txt
    """
    if gdb==None:
        if verbose:
            print "instantiating GraceDB instance for default server"
        gdb = GraceDb()
    raise Exception("WRITE ME")

###
def olibEventCreation( graceid, gdb=None, verbose=False ):
    """
    event creation sanity check for oLIB
    we check:
        trigger.json
    """
    raise Exception("WRITE ME")

###
def gstlalEventCreation( graceid, gdb=None, verbose=False ):
    """
    event creation sanity check for gstlal
    we check:
        coinc.xml
        psd.xml
    """
    raise Exception("WRITE ME")

###
def spiirEventCreation( graceid, gdb=None, verbose=False ):
    """
    event creation sanity check for gstlal-spiir
    we check:
        coinc.xml
        psd.xml
    """
    raise Exception("WRITE ME")

###
def mbtaEventCreation( graceid, gdb=None, verbose=False ):
    """
    event creation sanity check for MBTA
    we check:
        coinc.xml
        psd.xml
    """
    raise Exception("WRITE ME")

###
def pycbcEventCreation( graceid, gdb=None, verbose=False ):
    """
    event creation sanity check for pycbc
    we check:
        coinc.xml
        psd.xml
    """
    raise Exception("WRITE ME")

#------------------------
# FAR
#------------------------

class FARItem(utils.QueueItem):
    """
    a check for propper FAR
    """
    description = "check sanity of reported FAR"

    def __init__(self, graceid, gdb, t0, timeout, gdb=None, verbose=False):
        super(FARItem, self).__init__(graceid, t0, timeout, farCheck, description=self.description, gdb=gdb, verbose=verbose)

def farCheck( graceid, gdb=None, verbose=False ):
    """
    check the sanity of the reported FAR
    """
    raise Exception("WRITE ME")

#------------------------
# localRate
#------------------------

class LocalRateItem(utils.QueueItem):
    """
    a check for propper event creation and readability of associated trigger files
    """
    description = "check local rates of events"

    def __init__(self, graceid, gdb, group, pipeline, search, t0, timeout, gdb=None, verbose=False):
        super(LocalRateItem, self).__init__(graceid, t0, timeout, localRate, description=self.description, gdb=gdb, verbose=verbose)

def localRate( graceid, gdb=None, verbose=None ):
    """
    check the local rate of triggers submitted to GraceDB
    """
    raise Exception("WRITE ME")

#------------------------
# external triggers
#------------------------

class ExternalTriggersItem(utils.QueueItem):
    """
    a check that the external triggers search was completed
    """
    description = "check that the unblind injection search completed"

    def __init__(self, graceid, gdb, t0, timeout, gdb=None, verbose=False):
        super(ExternalTriggersItem, self).__init__(graceid, t0, timeout, externalTriggers, description=self.description, gdb=gdb, verbose=verbose)

def externalTriggers( graceid, gdb=None, verbose=False ):
    raise Exception("WRITE ME")

#------------------------
# unblind injections
#------------------------

class ExternalTriggers(utils.QueueItem):
    """
    a check that the unblind Injections search was completed
    """
    description = "check that the unblind injection search completed"

    def __init__(self, graceid, gdb, t0, timeout, gdb=None, verbose=False):
        super(UnblindInjectionsItem, self).__init__(graceid, t0, timeout, unblindInjections, description=self.description, gdb=gdb, verbose=verbose)

def unblindInjections( graceid, gdb=None, verbose=False ):
    raise Exception("WRITE ME")
