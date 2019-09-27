#!/usr/bin/env python
#Adapted from OnDA


try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import lib.onda.cfelpyutils.cfeloptarg as cfel_oa
from lib.onda.utils import (
    onda_optargs as onda_oa,
    global_params as gp,
    dynamic_import as dyn_imp
)

args = onda_oa.parse_onda_cmdline_args()

config = configparser.ConfigParser()
config.read(args.ini)

proc_params = cfel_oa.parse_parameters(config)
gp.monitor_params = proc_params

processing_layer = dyn_imp.import_layer_module('processing_layer', proc_params)
Coin = getattr(processing_layer, 'Coin')
proc = Coin(args.source, proc_params)
proc.start(verbose=False)
    
    
    
