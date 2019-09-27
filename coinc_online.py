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


if __name__ == "__main__":
 
    args = onda_oa.parse_onda_cmdline_args()

    config = configparser.ConfigParser()
    config.read(args.ini)

    monitor_params = cfel_oa.parse_parameters(config)
    gp.monitor_params = monitor_params

    processing_layer = dyn_imp.import_layer_module('processing_layer', monitor_params)
    Onda = getattr(processing_layer, 'Onda')

    mon = Onda(args.source, monitor_params)
    mon.start(verbose=False)
    
    
    import sys
    import numpy
    import signal
    import datetime
    import copy
    import pyqtgraph as pg
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)


    rec_ip = '172.21.50.21'
    rec_port = 12321

    _ = MainFrame(rec_ip, rec_port)
    sys.exit(app.exec_())
    
