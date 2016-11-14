#!/usr/bin/python
usage       = "eventSupervisor_assemblyTests.py [--options] config"
description = "a script testing how event supervisor assembles and manages a SortedQueue through parseAlert"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

import eventSupervisor.eventSupervisor as es
import eventSupervisor.eventSupervisorUtils as esUtils
import lvalertMP.lvalert.lvalertMPutils as utils

#------------------------

import time

from ConfigParser import SafeConfigParser

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

parser.add_option('-l', '--logDir', default='.', type='string', help='the directory into which log files will be written')
parser.add_option('-L', '--logLevel', default=10, type='int', help='the verbosity level of the logger. Lower numbers mean more output')
parser.add_option('', '--logTag', default='exeTest', type='string')

### check everything
parser.add_option('', '--everything', default=False, action="store_true", help="run tests for everything")

# notify
parser.add_option("", "--new", default=False, action="store_true")

# updates
parser.add_option("", "--fits", default=False, action="store_true")
parser.add_option("", "--skymapSummaryStart", default=False, action="store_true")

parser.add_option("", "--idqStart", default=False, action="store_true")
parser.add_option("", "--idqGlitchFAP", default=False, action="store_true")
parser.add_option("", "--idqActiveChan", default=False, action="store_true")

parser.add_option("", "--omegaScanStart", default=False, action="store_true")
parser.add_option("", "--segDbStart", default=False, action="store_true")

parser.add_option("", "--bayestarStart", default=False, action="store_true")
parser.add_option("", "--bayeswavePEStart", default=False, action="store_true")
parser.add_option("", "--lalinfStart", default=False, action="store_true")
parser.add_option("", "--libPEStart", default=False, action="store_true")

# labels

# signoffs

opts, args = parser.parse_args()

### finish parsing args
if len(args)!=1:
    raise ValueError('please supply exactly 1 input argument\n%s'%usage)
configname = args[0]

### finish parsing options
opts.new                = opts.new                or opts.everything
opts.fits               = opts.fits               or opts.everything
opts.skymapSummaryStart = opts.skymapSummaryStart or opts.everything
opts.idqStart           = opts.idqStart           or opts.everything
opts.idqGlitchFAP       = opts.idqGlitchFAP       or opts.everything
opts.idqActiveChan      = opts.idqActiveChan      or opts.everything
opts.omegaScanStart     = opts.omegaScanStart     or opts.everything
opts.segDbStart         = opts.segDbStart         or opts.everything
opts.bayestarStart      = opts.bayestarStart      or opts.everything
opts.bayeswavePEStart   = opts.bayeswavePEStart   or opts.everything
opts.lalinfStart        = opts.lalinfStart        or opts.everything
opts.libPEStart         = opts.libPEStart         or opts.everything

#-------------------------------------------------

if not os.path.exists(opts.logDir):
    os.makedirs( opts.logDir )
logger = logging.getLogger(opts.logTag)
logger.setLevel(opts.logLevel)

logname = utils.genLogname(opts.logDir, 'event_supervisor')

for handler in [logging.FileHandler(logname), logging.StreamHandler()]:
    handler.setFormatter( utils.genFormatter() )
    logger.addHandler( handler )

logger.debug( "writing log into : %s"%logname )

#-------------------------------------------------

### load config file
logger.info( "loading config from : %s"%configname )
config = SafeConfigParser()
config.read( configname )

#-------------------------------------------------

### SortedQueues that we play around with
queue          = utils.SortedQueue()
queueByGraceID = dict()

#-------------------------------------------------

if opts.new:
    logger.info("TESTING: new")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --new")

if opts.fits:
    raise NotImplementedError('need to format alert before this test will work!')

    logger.info("TESTING: fits")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --fits")

if opts.skymapSummaryStart:
    raise NotImplementedError('need to format alert before this test will work!')

    logger.info("TESTING: skymapSummaryStart")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --skymapSummaryStart")

if opts.idqStart:
    raise NotImplementedError('need to format alert before this test will work!')

    logger.info("TESTING: idqStart")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --idqStart")

if opts.idqGlitchFAP:
    raise NotImplementedError('need to format alert before this test will work!')

    logger.info("TESTING: idqGlitchFAP")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --idqGlitchFAP")

if opts.idqActiveChan:
    raise NotImplementedError('need to format alert before this test will work!')

    logger.info("TESTING: idqActiveChan")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --idqActiveChan")

if opts.omegaScanStart:
    raise NotImplementedError('need to format alert before this test will work!')

    logger.info("TESTING: omegaScanStart")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --omegaScanStart")

if opts.segDbStart:
    raise NotImplementedError('need to format alert before this test will work!')

    logger.info("TESTING: segDbStart")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --segDbStart")

if opts.bayestarStart:
    raise NotImplementedError('need to format alert before this test will work!')

    logger.info("TESTING: bayestarStart")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --bayestarStart")

if opts.bayeswavePEStart:
    raise NotImplementedError('need to format alert before this test will work!')

    logger.info("TESTING: bayeswavePEStart")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --bayeswavePEStart")

if opts.lalinfStart:
    raise NotImplementedError('need to format alert before this test will work!')

    logger.info("TESTING: lalinfStart")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --lalinfStart")

if opts.libPEStart:
    raise NotImplementedError('need to format alert before this test will work!')

    logger.info("TESTING: libPEStart")
    alert = {
             'uid'      : 'G123FAKE',
             'group'    : 'NOT',
             'pipeline' : 'REAL',
            }

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

    logger.info("passed all assertion statements for --libPEStart")
