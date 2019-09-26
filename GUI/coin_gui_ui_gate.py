
import sys
import numpy as np
import signal
import datetime
import copy
import pyqtgraph as pg



from UI.GUIs import TofGUI, XYGUI, XTGUI, YTGUI, PiPiCoGUI, eAGUI, eRGUI, eARGUI, eXYGUI

#from GateXY1 import GateXY1
#from GateXY2 import GateXY2
#from GateXY3 import GateXY3

from lib.onda.gui_utils.zmq_gui_utils import ZMQListener

from pyqtgraph.Qt import QtGui, QtCore

import matplotlib
from cmapToColormap import cmapToColormap

import copy
import time

class MainFrame(QtGui.QMainWindow):
    listening_thread_start_processing = QtCore.pyqtSignal()
    listening_thread_stop_processing = QtCore.pyqtSignal()
    
    def __init__(self, rec_ip, rec_port, monitor_params):
        super(MainFrame, self).__init__()

        self.rec_ip, self.rec_port = rec_ip, rec_port
        
        self.Xmin, self.Ymin, self.Tmin = monitor_params['OutputLayer']['xmin'],monitor_params['OutputLayer']['ymin'],monitor_params['OutputLayer']['tmin']
        self.Xmax, self.Ymax, self.Tmax = monitor_params['OutputLayer']['xmax'],monitor_params['OutputLayer']['ymax'],monitor_params['OutputLayer']['tmax']
        self.Xbin, self.Ybin, self.Tbin = monitor_params['OutputLayer']['xbin'],monitor_params['OutputLayer']['ybin'],monitor_params['OutputLayer']['tbin']
        
        self.Xbinnum = int((self.Xmax - self.Xmin)/self.Xbin)
        self.Ybinnum = int((self.Ymax - self.Ymin)/self.Ybin)
        self.Tbinnum = int((self.Tmax - self.Tmin)/self.Tbin)
        
        self.Xaxis  = np.linspace(self.Xmin, self.Xmax, self.Xbinnum)
        self.Yaxis = np.linspace(self.Ymin, self.Ymax, self.Ybinnum)
        self.Taxis = np.linspace(self.Tmin, self.Tmax, self.Tbinnum)
        
        self.Xaxis_r  = self.Xaxis[::-1]
        self.Yaxis_r = self.Yaxis[::-1]
        self.Taxis_r = self.Taxis[::-1]
 
        self.XaxisM = (self.Xaxis[:-1] + self.Xaxis[1:])/2
        self.YaxisM = (self.Yaxis[:-1] + self.Yaxis[1:])/2
        self.TaxisM = (self.Taxis[:-1] + self.Taxis[1:])/2
        
        
        self.eXmin, self.eYmin, self.eRmin, self.eAmin = monitor_params['OutputLayer']['exmin'],monitor_params['OutputLayer']['eymin'],monitor_params['OutputLayer']['ermin'],monitor_params['OutputLayer']['eamin']
        self.eXmax, self.eYmax, self.eRmax, self.eAmax = monitor_params['OutputLayer']['exmax'],monitor_params['OutputLayer']['eymax'],monitor_params['OutputLayer']['ermax'],monitor_params['OutputLayer']['eamax']
        self.eXbin, self.eYbin, self.eRbin, self.eAbin = monitor_params['OutputLayer']['exbin'],monitor_params['OutputLayer']['eybin'],monitor_params['OutputLayer']['erbin'],monitor_params['OutputLayer']['eabin']
        
        self.eXbinnum = int((self.eXmax - self.eXmin)/self.eXbin)
        self.eYbinnum = int((self.eYmax - self.eYmin)/self.eYbin)
        self.eAbinnum = int((self.eAmax - self.eAmin)/self.eAbin)
        self.eRbinnum = int((self.eRmax - self.eRmin)/self.eRbin)    
        
        print self.eAmax, self.eAmin    
        
        self.eXaxis  = np.linspace(self.eXmin, self.eXmax, self.eXbinnum)
        self.eYaxis = np.linspace(self.eYmin, self.eYmax, self.eYbinnum)
        self.eAaxis = np.linspace(self.eAmin, self.eAmax, self.eAbinnum)
        self.eRaxis = np.linspace(self.eRmin, self.eRmax, self.eRbinnum)        
        
        self.eXaxis_r  = self.eXaxis[::-1]
        self.eYaxis_r = self.eYaxis[::-1]
        self.eAaxis_r = self.eAaxis[::-1]
        self.eRaxis_r = self.eRaxis[::-1]        
 
        self.eXaxisM = (self.eXaxis[:-1] + self.eXaxis[1:])/2
        self.eYaxisM = (self.eYaxis[:-1] + self.eYaxis[1:])/2
        self.eAaxisM = (self.eAaxis[:-1] + self.eAaxis[1:])/2        
        self.eRaxisM = (self.eRaxis[:-1] + self.eRaxis[1:])/2                
                
        
      #  self.XY = np.zeros([self.Xbinnum-1, self.Ybinnum-1])
    #    self.Tof = np.zeros([self.Tbinnum-1,1])
        self.XT = np.zeros([self.Tbinnum-1, self.Xbinnum-1])
        self.YT = np.zeros([self.Tbinnum-1, self.Ybinnum-1])
        self.TSumX = np.zeros([self.Tbinnum-1,1])
        self.TSumY = np.zeros([self.Tbinnum-1,1])
        
 #       self.PiPiCo = np.zeros([self.Tbinnum-2,self.Tbinnum-2])


       # print self.PiPiCo.shape, '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
               
        self.pos, self.colors = zip(*cmapToColormap(matplotlib.cm.jet))
        # Set the colormap
        self.clrmp =  pg.ColorMap(self.pos, self.colors)


        
        self.TofGui = TofGUI(self)   
        self.TofGui.TofPlotWidget.scene().sigMouseMoved.connect(self.mouseMoved_Tof)
        self.TofGui.show()
                
                
        self.eXYGui = eXYGUI(self)                           
       # self.XYPlot = pg.ImageView(name='XY')
        self.eXYGui.eXYPlot.setColorMap(self.clrmp)                
      #  self.XYText = pg.LabelItem() 
      #  self.XYGui.XYPlot.addItem(self.XYText)
       # self.winXY.setCentralWidget(self.XYPlot)          
        self.eXYGui.eXYItem.scene().sigMouseMoved.connect(self.mouseMoved_eXY)
        self.eXYGui.eXYPlot.view.invertY(False)
        self.eXYGui.show()
        
        self.eRGui = eRGUI(self)                           
       # self.XYPlot = pg.ImageView(name='XY')

      #  self.XYText = pg.LabelItem() 
      #  self.XYGui.XYPlot.addItem(self.XYText)
       # self.winXY.setCentralWidget(self.XYPlot)          
        self.eRGui.eRPlotWidget.scene().sigMouseMoved.connect(self.mouseMoved_eR)
      #  self.eRGui.eRPlot.view.invertY(False)
        self.eRGui.show()
        
        self.eAGui = eAGUI(self)                           
       # self.XYPlot = pg.ImageView(name='XY')

      #  self.XYText = pg.LabelItem() 
      #  self.XYGui.XYPlot.addItem(self.XYText)
       # self.winXY.setCentralWidget(self.XYPlot)          
        self.eAGui.eAPlotWidget.scene().sigMouseMoved.connect(self.mouseMoved_eA)
       # self.eRGui.eARPlot.view.invertY(False)
        self.eAGui.show()           
        
        self.eARGui = eARGUI(self)                           
       # self.XYPlot = pg.ImageView(name='XY')
        self.eARGui.eARPlot.setColorMap(self.clrmp)                
      #  self.XYText = pg.LabelItem() 
      #  self.XYGui.XYPlot.addItem(self.XYText)
       # self.winXY.setCentralWidget(self.XYPlot)          
        self.eARGui.eARItem.scene().sigMouseMoved.connect(self.mouseMoved_eAR)
        self.eARGui.eARPlot.view.invertY(False)
        self.eARGui.show()                
                        
                
        self.XYGui = XYGUI(self)                           
       # self.XYPlot = pg.ImageView(name='XY')
        self.XYGui.XYPlot.setColorMap(self.clrmp)                
      #  self.XYText = pg.LabelItem() 
      #  self.XYGui.XYPlot.addItem(self.XYText)
       # self.winXY.setCentralWidget(self.XYPlot)          
        self.XYGui.XYItem.scene().sigMouseMoved.connect(self.mouseMoved_XY)
        self.XYGui.XYPlot.view.invertY(False)
        self.XYGui.show()
        
        self.XTGui = XTGUI()                   
       # self.XTPlot = pg.ImageView(name='XT')
        self.XTGui.XTPlot.setColorMap(self.clrmp)                
        self.XTText = pg.LabelItem() 
        self.XTGui.XTPlot.addItem(self.XTText)
       # self.winXT.setCentralWidget(self.XTPlot)          
        self.XTGui.XTItem.scene().sigMouseMoved.connect(self.mouseMoved_XT)
        self.XTGui.XTPlot.view.invertY(False)
        self.XTGui.show()     
        
        self.YTGui = YTGUI()                   
       # self.YTPlot = pg.ImageView(name='YT')
        self.YTGui.YTPlot.setColorMap(self.clrmp)                
        self.YTTeYT = pg.LabelItem() 
        self.YTGui.YTPlot.addItem(self.YTTeYT)
       # self.winYT.setCentralWidget(self.YTPlot)          
        self.YTGui.YTItem.scene().sigMouseMoved.connect(self.mouseMoved_YT)
        self.YTGui.YTPlot.view.invertY(False)
        self.YTGui.show()           
  
        self.PiPiCoGui = PiPiCoGUI(self)                   
       # self.PiPiCoPlot = pg.ImageView(name='PiPiCo')
        self.PiPiCoGui.PiPiCoPlot.setColorMap(self.clrmp)                
     #   self.PiPiCoTePiPiCo = pg.LabelItem() 
      #  self.PiPiCoGui.PiPiCoPlot.addItem(self.PiPiCoTePiPiCo)
       # self.winPiPiCo.setCentralWidget(self.PiPiCoPlot)          
        self.PiPiCoGui.PiPiCoItem.scene().sigMouseMoved.connect(self.mouseMoved_PiPiCo)
        self.PiPiCoGui.PiPiCoPlot.view.invertY(False)
        self.PiPiCoGui.show()
        
        
        
                                

        
        self.num_evts = 120
        
        self.num_shot = 0
        self.old_count = 0
        self.new_count = 0
        
        self.old_count_e = 0
        self.new_count_e = 0
                
        self.num_shots = 0
        
        
        self.data_dict = {}
        self.local_data_dict = {}
        
        self.tof_inds = []
        
        

        self.zeromq_listener_thread = QtCore.QThread()

      
        self.zeromq_listener = ZMQListener(self.rec_ip, self.rec_port, u'coin_data')
        self.init_listening_thread()
        
        self.refresh_timer = QtCore.QTimer()
        self.init_timer()

      #  self.show()
      
        self.old_time = time.time()
        self.total_num_shots = 0
        
        self.speed_rep_int = 120


    def init_listening_thread(self):
 #       self.zeromq_listener.moveToThread(self.zeromq_listener_thread)
        self.zeromq_listener.zmqmessage.connect(self.data_received)
        
    #    self.zeromq_listener.start_listening()
        
        self.listening_thread_start_processing.connect(self.zeromq_listener.start_listening)
        self.listening_thread_stop_processing.connect(self.zeromq_listener.stop_listening)
        
 #       self.zeromq_listener_thread.start()
        self.zeromq_listener.start()
        self.listening_thread_start_processing.emit()

    def init_timer(self):
        self.refresh_timer.timeout.connect(self.update_images)
        print 'start refresht timer'
        self.refresh_timer.start()

    def data_received(self, dat):
       # print 'data received'
        self.data_dict = copy.deepcopy(dat)
       # print self.data_dict.keys()
        #print self.data_dict['ion_hits'], self.data_dict['t_peaks']
        #print len(self.data_dict['ion_hits'])
        
                        
        self.tof_inds = []
        
        for ion_ind in range(len(self.data_dict['ion']['Xinds'])):            
       #     Tofind_l = np.where(self.Taxis >= self.newhit[0])[0][0]
       #     Xind_l = np.where(self.Xaxis >= self.newhit[1])[0][0]
       #     Yind_l = np.where(self.Yaxis >= self.newhit[2])[0][0]
            
            
            Tofind = self.data_dict['ion']['Tofinds'][ion_ind]-1
            Xind = self.data_dict['ion']['Xinds'][ion_ind]-1
            Yind = self.data_dict['ion']['Yinds'][ion_ind]-1
            
            self.tof_inds.append(Tofind)
            
            self.TofGui.Tof[Tofind] += 1
            self.XYGui.XY[Xind, Yind] += 1
            self.XT[Tofind, Xind] += 1
            self.YT[Tofind, Yind] += 1 
            
            
            #print self.XYGui.RectGate1.new_count, self.XYGui.RectGate1.old_count
            if self.PiPiCoGui.RectGate1_roiState == 1:

                self.PiPiCoGui.RectGate1.update_variables(Tofind)  
                self.PiPiCoGui.RectGate1.shot_num += 1
                if self.PiPiCoGui.RectGate1.shot_num == 1:
                    self.PiPiCoGui.RectGate1.old_count = self.PiPiCoGui.RectGate1.sum_under_2d_roi()
                if self.PiPiCoGui.RectGate1.shot_num == self.num_evts:
                    self.PiPiCoGui.RectGate1.new_count = self.PiPiCoGui.RectGate1.sum_under_2d_roi()
                    if self.PiPiCoGui.RectGate1.new_count is not None and self.PiPiCoGui.RectGate1.old_count is not None:
                        temp_rate = (self.PiPiCoGui.RectGate1.new_count - self.PiPiCoGui.RectGate1.old_count)/float(self.num_evts)
                        self.PiPiCoGui.PiPiCoUi.Rect1Rate.setText(self.PiPiCoGui.RectGate1.roiName+"Rate:%0.1f" % temp_rate)
                        self.PiPiCoGui.RectGate1.shot_num = 0 
                    
            if self.TofGui.RectGate1_roiState == 1:
                self.TofGui.RectGate1.update_ion(Tofind, Xind, Yind)  
                self.TofGui.RectGate1.shot_num += 1
                if self.TofGui.RectGate1.shot_num == 1:
                    self.TofGui.RectGate1.old_count = self.TofGui.RectGate1.sum_under_1d_roi()
                if self.TofGui.RectGate1.shot_num == self.num_evts:
                    self.TofGui.RectGate1.new_count = self.TofGui.RectGate1.sum_under_1d_roi()
                    if self.TofGui.RectGate1.new_count is not None and self.TofGui.RectGate1.old_count is not None:
                        temp_rate = (self.TofGui.RectGate1.new_count - self.TofGui.RectGate1.old_count)/float(self.num_evts)
                        self.TofGui.TofUi.Rect1Rate.setText(self.TofGui.RectGate1.roiName+"Rate:%0.1f" % temp_rate)    
                        self.TofGui.RectGate1.shot_num = 0       
                        
            if self.PiPiCoGui.RectGate2_roiState == 1:
                self.PiPiCoGui.RectGate2.update_variables(Tofind)  
                self.PiPiCoGui.RectGate2.shot_num += 1
                if self.PiPiCoGui.RectGate2.shot_num == 1:
                    self.PiPiCoGui.RectGate2.old_count = self.PiPiCoGui.RectGate2.sum_under_2d_roi()
                if self.PiPiCoGui.RectGate2.shot_num == self.num_evts:
                    self.PiPiCoGui.RectGate2.new_count = self.PiPiCoGui.RectGate2.sum_under_2d_roi()
                    if self.PiPiCoGui.RectGate2.new_count is not None and self.PiPiCoGui.RectGate2.old_count is not None:
                        temp_rate = (self.PiPiCoGui.RectGate2.new_count - self.PiPiCoGui.RectGate2.old_count)/float(self.num_evts)
                        self.PiPiCoGui.PiPiCoUi.Rect1Rate.setText(self.PiPiCoGui.RectGate2.roiName+"Rate:%0.1f" % temp_rate)
                        self.PiPiCoGui.RectGate2.shot_num = 0
                    
            if self.TofGui.RectGate2_roiState == 1:
                self.TofGui.RectGate2.update_ion(Tofind, Xind, Yind)  
                self.TofGui.RectGate2.shot_num += 1
                if self.TofGui.RectGate2.shot_num == 1:
                    self.TofGui.RectGate2.old_count = self.TofGui.RectGate2.sum_under_1d_roi()
                if self.TofGui.RectGate2.shot_num == self.num_evts:
                    self.TofGui.RectGate2.new_count = self.TofGui.RectGate2.sum_under_1d_roi()
                    if self.TofGui.RectGate2.new_count is not None and self.TofGui.RectGate2.old_count is not None:
                        temp_rate = (self.TofGui.RectGate2.new_count - self.TofGui.RectGate2.old_count)/float(self.num_evts)
                        self.TofGui.TofUi.Rect1Rate.setText(self.TofGui.RectGate2.roiName+"Rate:%0.1f" % temp_rate)  
                        self.TofGui.RectGate2.shot_num = 0
                        
                        
            if self.PiPiCoGui.RectGate3_roiState == 1:
                self.PiPiCoGui.RectGate3.update_variables(Tofind)  
                self.PiPiCoGui.RectGate3.shot_num += 1
                if self.PiPiCoGui.RectGate3.shot_num == 1:
                    self.PiPiCoGui.RectGate3.old_count = self.PiPiCoGui.RectGate3.sum_under_2d_roi()
                if self.PiPiCoGui.RectGate3.shot_num == self.num_evts:
                    self.PiPiCoGui.RectGate3.new_count = self.PiPiCoGui.RectGate3.sum_under_2d_roi()
                    if self.PiPiCoGui.RectGate3.new_count is not None and self.PiPiCoGui.RectGate3.old_count is not None:
                        temp_rate = (self.PiPiCoGui.RectGate3.new_count - self.PiPiCoGui.RectGate3.old_count)/float(self.num_evts)
                        self.PiPiCoGui.PiPiCoUi.Rect1Rate.setText(self.PiPiCoGui.RectGate3.roiName+"Rate:%0.1f" % temp_rate)
                        self.PiPiCoGui.RectGate3.shot_num = 0
                    
            if self.TofGui.RectGate3_roiState == 1:
                self.TofGui.RectGate3.update_ion(Tofind, Xind, Yind)  
                self.TofGui.RectGate3.shot_num += 1
                if self.TofGui.RectGate3.shot_num == 1:
                    self.TofGui.RectGate3.old_count = self.TofGui.RectGate3.sum_under_1d_roi()
                if self.TofGui.RectGate3.shot_num == self.num_evts:
                    self.TofGui.RectGate3.new_count = self.TofGui.RectGate3.sum_under_1d_roi()
                    if self.TofGui.RectGate3.new_count is not None and self.TofGui.RectGate3.old_count is not None:
                        temp_rate = (self.TofGui.RectGate3.new_count - self.TofGui.RectGate3.old_count)/float(self.num_evts)
                        self.TofGui.TofUi.Rect1Rate.setText(self.TofGui.RectGate3.roiName+"Rate:%0.1f" % temp_rate)  
                        self.TofGui.RectGate3.shot_num = 0                                                         
            
            
        for e_ind in range(len(self.data_dict['e']['eXinds'])):
        
            eAind = self.data_dict['e']['eAinds'][e_ind]-1
            eRind = self.data_dict['e']['eRinds'][e_ind]-1
            eXind = self.data_dict['e']['eXinds'][e_ind]-1
            eYind = self.data_dict['e']['eYinds'][e_ind]-1
            
        
          
            

            self.eXYGui.eXY[eXind, eYind] += 1
            self.eARGui.eAR[eAind, eRind] += 1
            
        for e_ind_f in range(len(self.data_dict['e']['eXinds_f'])):            
            
            eAind_f = self.data_dict['e']['eAinds_f'][e_ind_f]-1
            eRind_f = self.data_dict['e']['eRinds_f'][e_ind_f]-1
            eXind_f = self.data_dict['e']['eXinds_f'][e_ind_f]-1
            eYind_f = self.data_dict['e']['eYinds_f'][e_ind_f]-1    
            
            self.eAGui.eA[eAind_f] += 1            
            self.eRGui.eR[eRind_f] += 1                      
            
            
            if self.PiPiCoGui.RectGate1_roiState == 1:
                if self.PiPiCoGui.RectGate1.coin():
                    self.PiPiCoGui.RectGate1.update_electron(eAind_f, eRind_f, eXind_f, eYind_f)
                    
            if self.TofGui.RectGate1_roiState == 1:
                if self.TofGui.RectGate1.coin():
                    self.TofGui.RectGate1.update_electron(eAind_f, eRind_f, eXind_f, eYind_f)          
                    
            if self.PiPiCoGui.RectGate2_roiState == 1:
                if self.PiPiCoGui.RectGate2.coin():
                    self.PiPiCoGui.RectGate2.update_electron(eAind_f, eRind_f, eXind_f, eYind_f)
                    
            if self.TofGui.RectGate2_roiState == 1:
                if self.TofGui.RectGate2.coin():
                    self.TofGui.RectGate2.update_electron(eAind_f, eRind_f, eXind_f, eYind_f)    
                    
            if self.PiPiCoGui.RectGate3_roiState == 1:
                if self.PiPiCoGui.RectGate3.coin():
                    self.PiPiCoGui.RectGate3.update_electron(eAind_f, eRind_f, eXind_f, eYind_f)
                    
            if self.TofGui.RectGate3_roiState == 1:
                if self.TofGui.RectGate3.coin():
                    self.TofGui.RectGate3.update_electron(eAind_f, eRind_f, eXind_f, eYind_f)                                                

        
        if self.TofGui.RectGate1_roiState == 1:
            self.TofGui.RectGate1.reset_coin_var()   
                     
                     
        if self.PiPiCoGui.RectGate1_roiState == 1:                     
            self.PiPiCoGui.RectGate1.reset_coin_var()                      
            
        if self.TofGui.RectGate2_roiState == 1:
            self.TofGui.RectGate2.reset_coin_var()   
                     
                     
        if self.PiPiCoGui.RectGate2_roiState == 1:                     
            self.PiPiCoGui.RectGate2.reset_coin_var() 
            
        if self.TofGui.RectGate3_roiState == 1:
            self.TofGui.RectGate3.reset_coin_var()   
                     
                     
        if self.PiPiCoGui.RectGate3_roiState == 1:                     
            self.PiPiCoGui.RectGate3.reset_coin_var()                         

        
        self.tof_inds = sorted(self.tof_inds)    
        if len(self.tof_inds) > 1:
            for i_tof_ind in range(len(self.tof_inds)-1):
             #   print '****************************************',self.PiPiCo.shape, len(self.tof_inds)
                self.PiPiCoGui.PiPiCo[self.tof_inds[i_tof_ind],self.tof_inds[(i_tof_ind+1):]]  += 1                
           # print self.PiPiCo.shape
           
     #   self.XYGui.RectGate1.update_PiPiCo()    
        
       

        self.data_dict = {}
        
        self.total_num_shots += 1
        self.num_shot += 1
        
        if self.num_shot == 1:
            self.old_count = np.sum(self.TofGui.Tof)
            self.old_count_e = np.sum(self.eXYGui.eXY)
        if self.num_shot == self.num_evts:
            self.new_count = np.sum(self.TofGui.Tof)
            self.new_count_e = np.sum(self.eXYGui.eXY)
            
            total_rate = (self.new_count - self.old_count)/self.num_evts
        #    for lb in self.total_rate_labels:
            self.TofGui.TofUi.TotalRate.setText("TotalRate:%0.1f" % total_rate)
            self.XYGui.XYUi.TotalRate.setText("TotalRate:%0.1f" % total_rate)
            self.XTGui.XTUi.TotalRate.setText("TotalRate:%0.1f" % total_rate)
            self.YTGui.YTUi.TotalRate.setText("TotalRate:%0.1f" % total_rate)
            self.PiPiCoGui.PiPiCoUi.TotalRate.setText("TotalRate:%0.1f" % total_rate)                                                
            
            total_rate_e = (self.new_count_e - self.old_count_e)/self.num_evts
        #    for lb in self.total_rate_labels:
            self.eXYGui.eXYUi.TotalRate.setText("TotalRate:%0.1f" % total_rate_e)
            self.eARGui.eARUi.TotalRate.setText("TotalRate:%0.1f" % total_rate_e)
            self.eAGui.eAUi.TotalRate.setText("TotalRate:%0.1f" % total_rate_e)
            self.eRGui.eRUi.TotalRate.setText("TotalRate:%0.1f" % total_rate_e)                                    
            
            self.num_shot = 0
            
        
        self.num_shots = self.num_shots + 1

          


    def update_images(self):
    
       # QtGui.QApplication.processEvents()
        
        QtGui.QApplication.processEvents()
        
        self.TofGui.TofCurve.setData(np.squeeze(self.TaxisM),np.squeeze(self.TofGui.Tof))
        
        self.eAGui.eACurve.setData(np.squeeze(self.eAaxisM),np.squeeze(self.eAGui.eA))
        
        self.eRGui.eRCurve.setData(np.squeeze(self.eRaxisM),np.squeeze(self.eRGui.eR))
        
        
        QtGui.QApplication.processEvents()
        
        self.max_eXY = self.eXYGui.eXY.max()
        self.eXY_norm = self.eXYGui.eXY
     #   pos_XY = np.array([0.0, max_XY/2, max_XY])
     #   color_XY = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XY = pg.ColorMap(pos_XY, color_XY)  
     #   self.XYPlot.setColorMap(clrmp_XY)           
        if self.max_eXY != 0:  
            self.eXY_norm = self.eXYGui.eXY/self.max_eXY   
            self.eXYGui.eXYPlot.setImage(self.eXY_norm, autoRange = False, pos = [self.eXmin, self.eYmin], scale = [self.eXbin, self.eYbin])
            
          #  self.eXYGui.RectGate1.sum_under_2d_roi()
            
        self.max_eAR = self.eARGui.eAR.max()
        self.eAR_norm = self.eARGui.eAR
     #   pos_XY = np.array([0.0, max_XY/2, max_XY])
     #   color_XY = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XY = pg.ColorMap(pos_XY, color_XY)  
     #   self.XYPlot.setColorMap(clrmp_XY)           
        if self.max_eAR != 0:  
            self.eAR_norm = self.eARGui.eAR/self.max_eAR   
            self.eARGui.eARPlot.setImage(self.eAR_norm, autoRange = False, pos = [self.eAmin, self.eRmin], scale = [self.eAbin, self.eRbin])
            self.eARGui.eARItem.setAspectLocked(False)
         #   self.eARGui.RectGate1.sum_under_2d_roi()
         
        QtGui.QApplication.processEvents()
                                
                        
        self.max_XY = self.XYGui.XY.max()
        self.XY_norm = self.XYGui.XY
     #   pos_XY = np.array([0.0, max_XY/2, max_XY])
     #   color_XY = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XY = pg.ColorMap(pos_XY, color_XY)  
     #   self.XYPlot.setColorMap(clrmp_XY)           
        if self.max_XY != 0:  
            self.XY_norm = self.XYGui.XY/self.max_XY   
            self.XYGui.XYPlot.setImage(self.XY_norm, autoRange = False, pos = [self.Xmin, self.Ymin], scale = [self.Xbin, self.Ybin])
            
      #      self.XYGui.RectGate1.sum_under_2d_roi()
            
            
        #    self.tr = self.coord_transform(self.XY, self.XYGui.XYPlot.getImageItem(), axes=(0,1))
            #self.XYItem.setAspectLocked(False)
            #self.XYPlot.setImage(self.XY/max_XY, autoRange = False)
        
        self.max_XT = self.XT.max()
     #   pos_XT = np.array([0.0, max_XT/2, max_XT])
     #   color_XT = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XT = pg.ColorMap(pos_XY, color_XT)  
     #   self.XTPlot.setColorMap(clrmp_XT)   
        if self.max_XT != 0:                            
            self.XTGui.XTPlot.setImage(self.XT/self.max_XT, autoRange = False, pos = [self.Tmin, self.Xmin], scale = [self.Tbin, self.Xbin])
            self.XTGui.XTItem.setAspectLocked(False)
            
            
        QtGui.QApplication.processEvents()    
        
        self.max_YT = self.YT.max()
     #   pos_YT = np.array([0.0, max_YT/2, max_YT])
     #   color_YT = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_YT = pg.ColorMap(pos_YT, color_YT)
     #   self.YTPlot.setColorMap(clrmp_YT)  
        if self.max_YT != 0:         
            self.YTGui.YTPlot.setImage(self.YT/self.max_YT, autoRange = False, pos = [self.Tmin, self.Ymin], scale = [self.Tbin, self.Ybin])
            self.YTGui.YTItem.setAspectLocked(False)
            
        self.max_PiPiCo = self.PiPiCoGui.PiPiCo.max()
     #   pos_PiPiCo = np.array([0.0, max_PiPiCo/2, max_PiPiCo])
     #   color_PiPiCo = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubPiPiCoe)
     #   clrmp_PiPiCo = pg.ColorMap(pos_PiPiCo, color_PiPiCo)
     #   self.PiPiCoPlot.setColorMap(clrmp_PiPiCo)  
        if self.max_PiPiCo != 0:         
            self.PiPiCoGui.PiPiCoPlot.setImage(self.PiPiCoGui.PiPiCo/self.max_PiPiCo, autoRange = False, pos = [self.Tmin, self.Tmin], scale = [self.Tbin, self.Tbin])
            self.PiPiCoGui.PiPiCoItem.setAspectLocked(False)  
            
        temp_sum_ion =  np.sum(self.XYGui.XY)   
        self.PiPiCoGui.PiPiCoUi.TotalYield.setText("TotalYield:%0.1f" % temp_sum_ion)           
        self.XYGui.XYUi.TotalYield.setText("TotalYield:%0.1f" % temp_sum_ion)      
        self.XTGui.XTUi.TotalYield.setText("TotalYield:%0.1f" % temp_sum_ion)    
        self.YTGui.YTUi.TotalYield.setText("TotalYield:%0.1f" % temp_sum_ion)                     
        self.TofGui.TofUi.TotalYield.setText("TotalYield:%0.1f" % temp_sum_ion)               
        
        temp_sum_e =  np.sum(self.eXYGui.eXY)   
        self.eXYGui.eXYUi.TotalYield.setText("TotalYield:%0.1f" % temp_sum_e)           
        self.eARGui.eARUi.TotalYield.setText("TotalYield:%0.1f" % temp_sum_e)      
        self.eAGui.eAUi.TotalYield.setText("TotalYield:%0.1f" % temp_sum_e)    
        self.eRGui.eRUi.TotalYield.setText("TotalYield:%0.1f" % temp_sum_e)                     

                
                       
            
        if True and self.PiPiCoGui.RectGate1_roiState == 1:    
            self.PiPiCoGui.RectGate1.update_plots()    
       #     self.PiPiCoGui.PiPiCoUi.Rect1Yield.setText(self.PiPiCoGui.RectGate1.roiName+"Yield:%0.1f" % self.PiPiCoGui.RectGate1.sum_under_2d_roi())
            
        if True and self.TofGui.RectGate1_roiState == 1:    
            self.TofGui.RectGate1.update_plots()            
         #   self.TofGui.TofUi.Rect1Yield.setText(self.TofGui.RectGate1.roiName+"Yield:%0.1f" % self.TofGui.RectGate1.sum_under_1d_roi())         
            
        if True and self.PiPiCoGui.RectGate2_roiState == 1:    
            self.PiPiCoGui.RectGate2.update_plots()    
           # self.PiPiCoGui.PiPiCoUi.Rect2Yield.setText(self.PiPiCoGui.RectGate2.roiName+"Yield:%0.1f" % self.PiPiCoGui.RectGate2.sum_under_2d_roi())            
            
        if True and self.TofGui.RectGate2_roiState == 1:    
            self.TofGui.RectGate2.update_plots()   
         #   self.TofGui.TofUi.Rect2Yield.setText(self.TofGui.RectGate2.roiName+"Yield:%0.1f" % self.TofGui.RectGate2.sum_under_1d_roi())         
               
            
        if True and self.PiPiCoGui.RectGate3_roiState == 1:    
            self.PiPiCoGui.RectGate3.update_plots()    
         #   self.PiPiCoGui.PiPiCoUi.Rect3Yield.setText(self.PiPiCoGui.RectGate3.roiName+"Yield:%0.1f" % self.PiPiCoGui.RectGate3.sum_under_2d_roi())            
            
        if True and self.TofGui.RectGate3_roiState == 1:    
            self.TofGui.RectGate3.update_plots()  
          #  self.TofGui.TofUi.Rect3Yield.setText(self.TofGui.RectGate3.roiName+"Yield:%0.1f" % self.TofGui.RectGate3.sum_under_1d_roi())                                                
            
     #   print self.total_num_shots
            
        if self.total_num_shots % self.speed_rep_int < 10:
            self.time = time.time()
            print('Processed: {0} in {1:.2f} seconds ({2:.2f} Hz)'.format(
                self.total_num_shots,
                self.time - self.old_time,
                float(self.speed_rep_int)/float(self.time-self.old_time)))
            sys.stdout.flush()
            self.old_time = self.time
            
        QtGui.QApplication.processEvents()    

                
    def mouseMoved_XY(self,pos):
        #print "X, Y:", self.
        #mousePoint = self.XYItem.mapFromScene(pos)
        mousePoint = self.XYGui.XYItem.vb.mapSceneToView(pos)
        self.XYGui.XYUi.MousePosition.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))     
        
    def mouseMoved_eXY(self,pos):
        #print "X, Y:", self.
        #mousePoint = self.XYItem.mapFromScene(pos)
        mousePoint = self.eXYGui.eXYItem.vb.mapSceneToView(pos)
        self.eXYGui.eXYUi.MousePosition.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))       
        
    def mouseMoved_eAR(self,pos):
        #print "X, Y:", self.
        #mousePoint = self.XYItem.mapFromScene(pos)
        mousePoint = self.eARGui.eARItem.vb.mapSceneToView(pos)
        self.eARGui.eARUi.MousePosition.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))                          
       
        
    def mouseMoved_Tof(self,pos):
        #print "X, Y:", self.
        mousePoint = self.TofGui.TofCurve.mapFromScene(pos)
        #mousePoint = self.TofGui.TofCurve.mapSceneToItem(pos)
        self.TofGui.TofUi.MousePosition.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))        
        
    def mouseMoved_eA(self,pos):
        #print "X, Y:", self.
        mousePoint = self.eAGui.eACurve.mapFromScene(pos)
        #mousePoint = self.TofGui.TofCurve.mapSceneToItem(pos)
        self.eAGui.eAUi.MousePosition.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))     
        
    def mouseMoved_eR(self,pos):
        #print "X, Y:", self.
        mousePoint = self.eAGui.eACurve.mapFromScene(pos)
        #mousePoint = self.TofGui.TofCurve.mapSceneToItem(pos)
        self.eAGui.eAUi.MousePosition.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))          
                
        
        
    def mouseMoved_PiPiCo(self,pos):
        #print "X, Y:", self.
        #mousePoint = self.PiPiCoItem.mapFromScene(pos)
        mousePoint = self.PiPiCoGui.PiPiCoItem.vb.mapSceneToView(pos)
        self.PiPiCoGui.PiPiCoUi.MousePosition.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))
        
    def mouseMoved_XT(self,pos):
        #print "X, Y:", self.
        #mousePoint = self.XTItem.mapFromScene(pos)
        mousePoint = self.XTGui.XTItem.vb.mapSceneToView(pos)
        self.XTGui.XTUi.MousePosition.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))        
        
    def mouseMoved_YT(self,pos):
        #print "X, Y:", self.
        #mousePoint = self.YTItem.mapFromScene(pos)
        mousePoint = self.YTGui.YTItem.vb.mapSceneToView(pos)
        self.YTGui.YTUi.MousePosition.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))        
                




def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    print 'sys.arv:',len(sys.argv)
    if len(sys.argv) == 1:
        #rec_ip = '198.129.217.74'
        #rec_ip = '10.0.0.12'
       # rec_ip = '2601:647:4c02:a620:14e8:72a9:d37:fe00'
        rec_ip = '172.21.49.249'
        rec_port = 12321
    elif len(sys.argv) == 3:
        rec_ip = sys.argv[1]
        rec_port = int(sys.argv[2])
    else:
        print('Usage: onda-photofragmentation_gui.py <listening ip> <listening port>')
        sys.exit()

    _ = MainFrame(rec_ip, rec_port)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
