#!/usr/bin/python
usage       = "eventSupervisor_assemblyTests.py [--options] config"
description = "a script testing how event supervisor assembles and manages a SortedQueue through parseAlert"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

import eventSupervisor.eventSupervisor as es
import eventSupervisor.eventSupervisorUtils as esUtils
import lvalertMP.lvalert.lvalertMPutils as utils

#------------------------

import os

import logging

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
parser.add_option("", "--psd", default=False, action='store_true')

parser.add_option("", "--fits", default=False, action="store_true")

parser.add_option("", "--snglFITSStart", default=False, action="store_true")
parser.add_option("", "--snglFITSFinish", default=False, action="store_true")
parser.add_option("", "--multFITSStart", default=False, action="store_true")

parser.add_option("", "--idqStart", default=False, action="store_true")
parser.add_option("", "--idqGlitchFAP", default=False, action="store_true")
parser.add_option("", "--idqActiveChan", default=False, action="store_true")

parser.add_option("", "--omegaScanStart", default=False, action="store_true")
parser.add_option("", "--segDbStart", default=False, action="store_true")

parser.add_option("", "--bayestarStart", default=False, action="store_true")
parser.add_option("", "--bayestarSkymap", default=False, action="store_true")
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
opts.psd                = opts.psd                or opts.everything
opts.fits               = opts.fits               or opts.everything
opts.snglFITSStart      = opts.snglFITSStart      or opts.everything
opts.snglFITSFinish     = opts.snglFITSFinish     or opts.everything
opts.multFITSStart      = opts.multFITSStart      or opts.everything
opts.idqStart           = opts.idqStart           or opts.everything
opts.idqGlitchFAP       = opts.idqGlitchFAP       or opts.everything
opts.idqActiveChan      = opts.idqActiveChan      or opts.everything
opts.omegaScanStart     = opts.omegaScanStart     or opts.everything
opts.segDbStart         = opts.segDbStart         or opts.everything
opts.bayestarStart      = opts.bayestarStart      or opts.everything
opts.bayestarSkymap     = opts.bayestarSkymap     or opts.everything
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

if opts.new:
    logger.info("TESTING: new")
    alert = {
             'alert_type' : 'new',
             'uid'        : 'G123FAKE',
             'object'     : {'group'    : 'CBC',
                             'pipeline' : 'gstlal',
                             'far'      : 1e-8,
                            },
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    for name in es.new:
        for i, item in enumerate(queue):
            if item.name==name:
                queue.pop( i )
                break
        else:
            assert False, 'could not find item corresponding to name=%s'%name
    assert len(queue)==0, 'queue should be empty at this point'

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'
    
    logger.info("passed all assertion statements for --new")

#-------------------------------------------------

if opts.psd:
    logger.info("TESTING: psd")
    alert = {
             'alert_type' : 'update',
             'uid'        : 'G123FAKE',
             'object'     : {'group'    : 'CBC',
                             'pipeline' : 'gstlal',
                             'far'      : 1e-8,
                            },
             'description': 'DOES NOT MATTER',
             'file'       : 'psd.xml.gz',
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    assert len(queue)==3, "should be 3 items in the queue"
    names = [name for name in es.parent_child['psd']] ### make a copy
    for item in queue:
        assert item.name in names, "must the the correct type"
        names.remove( item.name )
    assert len(names)==0, "this should have gotten rid of all the names"

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    assert len(queue)==3
    names = [name for name in es.parent_child['psd']] ### make a copy
    for item in queue:
        assert item.name in names, "must the the correct type"
        names.remove( item.name )
    assert len(names)==0, "this should have gotten rid of all the names"

    logger.info("passed all assertion statements for --psd")

#-------------------------------------------------

if opts.fits:

    logger.info("TESTING: fits")
    alert = {
             'alert_type'  : 'update',
             'uid'         : 'G123FAKE',
             'description' : 'a meaningless description meant to avoid triggering anything',
             'file'        : 'fake.fits.gz',
             'object'      : {'tag_names':['faketag'],
                              'group'    : 'CBC',
                              'pipeline' : 'gstlal',
                             },
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    for name in es.fits:
        for i, item in enumerate(queue):
            if item.name==name:
                queue.pop(i)
                break
            else:
                assert False, 'could not find item corresponding to name=%s'%name
    assert len(queue)==0, 'queue should be empty at this point'

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    for name in es.fits:
        for i, item in enumerate(queue):
            if item.name==name:
                queue.pop(i)
                break
            else:
                assert False, 'could not find item corresponding to name=%s'%name
    assert len(queue)==0, 'queue should be empty at this point'

    logger.info("passed all assertion statements for --fits")

#-------------------------------------------------

if opts.snglFITSStart:

    logger.info("TESTING: snglFITSStart")

    fitsname = "G123FAKE"
    alert = {
             'alert_type'  : 'update',
             'uid'         : 'G12345',
             'description' : 'started skymap summary for <a href="does not matter">%s</a>'%fitsname,
             'file'        : '',
             'object'      : {'tag_names' : 'does not matter'
                             },
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    assert len(queue)==1, "should be a single item in the queue"
    assert queue[0].name == 'snglFITS', "must be of the correct type"

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    assert len(queue)==1
    assert queue[0].name == 'snglFITS'

    logger.info("passed all assertion statements for --snglFITSStart")

#-------------------------------------------------

if opts.snglFITSFinish:

    logger.info('TESTING: snglFITSFinish')

    fitsname = "G123FAKE"
    alert = {
             'alert_type'  : 'update',
             'uid'         : 'G263554', ### extracted this by hand from https://gracedb.ligo.org -> may be fragile!
             'description' : 'finished skymap summary for <a href="does not matter">%s</a>'%fitsname,
             'file'        : '',
             'object'      : {'tag_names' : 'does not matter'
                             },
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    assert len(queue)==1, "should be a single item in the queue"
    assert queue[0].name == 'multFITS start', "must be of the correct type"

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    assert len(queue)==1
    assert queue[0].name == 'multFITS start'

    logger.info("passed all assertion statements for --snglFITSFinish")

#-------------------------------------------------

if opts.multFITSStart:

    logger.info('TESTING: multFITSStart')

    fitsname = "G123FAKE"
    alert = {
             'alert_type'  : 'update',
             'uid'         : 'G12345', 
             'description' : 'started skymap comparison for <a href="does not matter">fake.fits.gz</a>, <a href="unimportant">faker.fits</a>',
             'file'        : '',
             'object'      : {'tag_names' : 'does not matter'
                             },
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    assert len(queue)==1, "should be a single item in the queue"
    assert queue[0].name == 'multFITS', "must be of the correct type"

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    assert len(queue)==1
    assert queue[0].name == 'multFITS'

    logger.info("passed all assertion statements for --multFITS")

#-------------------------------------------------

if opts.idqStart:

    logger.info("TESTING: idqStart")
    alert = {
             'alert_type'  : 'update',
             'uid'         : 'G123FAKE',
             'object' : {'group'       : 'CBC',
                         'pipeline'    : 'gstlal',
                         },
             'description' : 'Started searching for iDQ information within [1162558843.270, 1162558843.370] at H1',
             'file'        : '',
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    assert len(queue)==1
    assert queue[0].name=='idq'

    queue = queueByGraceID[alert['uid']]
    assert len(queue)==1
    assert queue[0].name == 'idq'

    logger.info("passed all assertion statements for --idqStart")

#-------------------------------------------------

if opts.idqGlitchFAP:

    logger.info("TESTING: idqGlitchFAP")
    alert = {
             'alert_type'  : 'update',
             'uid'         : 'G123FAKE',
             'object' : {'group'       : 'CBC',
                         'pipeline'    : 'gstlal',
                        },
             'description' : 'minimum glitch-FAP for ovl at H1 within [1162558843.270, 1162558843.370] is 1.000e+00',
             'file'        : 'https://gracedb.ligo.org/apiweb/events/G260778/files/H1_ovl_minFAP_G260778-1162558843-0.json',
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    assert len(queue)==0, 'should ignore this alert because approval processor checks are not implemented'
    assert len(queueByGraceID.keys())==0

    logger.info("passed all assertion statements for --idqGlitchFAP")

#-------------------------------------------------

if opts.idqActiveChan:

    logger.info("TESTING: idqActiveChan")
    alert = {
             'alert_type'  : 'update',
             'uid'         : 'G123FAKE',
             'object' : {'group'       : 'CBC',
                         'pipeline'    : 'gstlal',
                        },
             'description' : 'iDQ (possible) active channels for ovl at L1 between [1162558838.320, 1162558848.320]',
             'file'        : 'https://gracedb.ligo.org/apiweb/events/G260778/files/L1_ovl_chanlist_G260778-1162558838-10.json',
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    assert len(queue)==0, 'should ignore this alert because idqOmegaScans are not implemented'
    assert len(queueByGraceID.keys())==0

    logger.info("passed all assertion statements for --idqActiveChan")

#-------------------------------------------------

if opts.omegaScanStart:

    logger.info("TESTING: omegaScanStart")

    name = 'l1 omega scan' ### only check L1, assume H1 and CIT work too...

    alert = {
             'alert_type'  : 'update',
             'uid'         : 'G123FAKE',
             'object' : {'group'       : 'CBC',
                         'pipeline'    : 'gstlal',
                         'comment' : 'automatic OmegaScans begun for: %s'%(', '.join(config.get(name+' start', 'chansets').split())),
                        },
             'description' : 'automatic OmegaScans begun for: %s'%(', '.join(config.get(name+' start', 'chansets').split())),
             'file'        : '',
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    assert len(queue)==1
    assert queue[0].name==name

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    assert len(queue)==1
    assert queue[0].name==name

    logger.info("passed all assertion statements for --omegaScanStart")

#-------------------------------------------------

if opts.segDbStart:

    logger.info("TESTING: segDbStart")
    alert = {
             'alert_type'  : 'update',
             'uid'         : 'G123FAKE',
             'object' : {'group'       : 'CBC',
                         'pipeline'    : 'gstlal',
                        },
             'description' : 'began searching for segments in : https://segments.ligo.org',
             'file'        : '', 
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    name = 'segdb2grcdb'

    assert len(queue)==1
    assert queue[0].name==name

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    assert len(queue)==1
    assert queue[0].name==name

    logger.info("passed all assertion statements for --segDbStart")

#-------------------------------------------------

if opts.bayestarStart:

    logger.info("TESTING: bayestarStart")
    alert = {
             'alert_type' : 'update',
             'uid'      : 'G123FAKE',
             'object' : {'group'    : 'CBC',
                         'pipeline' : 'gstlal',
                        },
             'description' : 'INFO:BAYESTAR:starting sky localization',
             'file'        : '',
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    name = 'bayestar'

    assert len(queue)==1
    assert queue[0].name==name

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    assert len(queue)==1
    assert queue[0].name==name

    logger.info("passed all assertion statements for --bayestarStart")

#-------------------------------------------------

if opts.bayestarSkymap:

    logger.info("TESTING: bayestarSkymap")
    alert = {
             'alert_type' : 'update',
             'uid'      : 'G123FAKE',
             'object' : {'tag_names':['faketag'],
                         'group'    : 'CBC',
                         'pipeline' : 'gstlal',
                        },
             'description' : 'INFO:BAYESTAR:uploaded sky map',
             'file'        : 'bayestar.fits.gz',
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    for name in es.fits+['bayestar finish']:
        for i, item in enumerate(queue):
            if item.name==name:
                queue.pop(i)
                break
            else:
                assert False, 'could not find item corresponding to name=%s'%name
    assert len(queue)==0, 'queue should be empty at this point'

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    for name in es.fits+['bayestar finish']:
        for i, item in enumerate(queue):
            if item.name==name:
                queue.pop(i)
                break
            else:
                assert False, 'could not find item corresponding to name=%s'%name
    assert len(queue)==0, 'queue should be empty at this point'

    logger.info("passed all assertion statements for --bayestarSkymap")

#-------------------------------------------------

if opts.bayeswavePEStart:

    logger.info("TESTING: bayeswavePEStart")
    alert = {
             'alert_type' : 'update',
             'uid'      : 'G123FAKE',
             'object' : {'group'    : 'CBC',
                         'pipeline' : 'gstlal',
                        },
             'description' : 'BayesWaveBurst launched',
             'file'        : '',
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    name = 'bayeswave pe'

    assert len(queue)==1
    assert queue[0].name==name

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    assert len(queue)==1
    assert queue[0].name==name

    logger.info("passed all assertion statements for --bayeswavePEStart")

#-------------------------------------------------

if opts.lalinfStart:

    logger.info("TESTING: lalinfStart")
    alert = {
             'alert_type' : 'update',
             'uid'      : 'G123FAKE',
             'object' : {'group'    : 'CBC',
                         'pipeline' : 'gstlal',
                        },
             'description' : 'LALInference online estimation started',
             'file'        : '',
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    name = 'lalinf'

    assert len(queue)==1
    assert queue[0].name==name

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    assert len(queue)==1
    assert queue[0].name==name

    logger.info("passed all assertion statements for --lalinfStart")

#-------------------------------------------------

if opts.libPEStart:

    logger.info("TESTING: libPEStart")
    alert = {
             'alert_type' : 'update',
             'uid'      : 'G123FAKE',
             'object' : {'group'    : 'CBC',
                         'pipeline' : 'gstlal',
                        },
             'description' : 'LIB Parameter estimation started.',
             'file'        : '',
            }
    queue          = utils.SortedQueue()
    queueByGraceID = dict()

    completed = es.parseAlert( queue, queueByGraceID, alert, time.time(), config, logTag=opts.logTag )

    name = 'lib pe'

    assert len(queue)==1
    assert queue[0].name==name

    assert len(queueByGraceID.keys())==1, 'there should be only one key here'
    assert queueByGraceID.has_key(alert['uid']), 'that key should be this one'

    queue = queueByGraceID[alert['uid']]
    assert len(queue)==1
    assert queue[0].name==name

    logger.info("passed all assertion statements for --libPEStart")
