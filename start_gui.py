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

from GUI.coin_gui_ui_gate_MCP import MainFrame


args = onda_oa.parse_onda_cmdline_args()

config = configparser.ConfigParser()
config.read(args.ini)
monitor_params = cfel_oa.parse_parameters(config)

    
    
import sys
import numpy
import signal
import datetime
import copy
import pyqtgraph as pg
    
from GUI.utils.zmq_gui_utils import ZMQListener


from pyqtgraph.Qt import QtGui, QtCore
    
signal.signal(signal.SIGINT, signal.SIG_DFL)
app = QtGui.QApplication(sys.argv)


rec_ip = '172.21.49.249'
rec_port = 12321
_ = MainFrame(rec_ip, rec_port, monitor_params)
sys.exit(app.exec_())
