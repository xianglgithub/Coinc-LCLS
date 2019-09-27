
import sys
import numpy as np
import signal
import datetime
import copy
import pyqtgraph as pg
import matplotlib
import h5py

import  time

from UI.GUIs import TofGUI, XYGUI, XTGUI, YTGUI, PiPiCoGUI, ControlPanel

from lib.onda.gui_utils.zmq_gui_utils import ZMQListener

from pyqtgraph.Qt import QtGui, QtCore

from cmapToColormap import cmapToColormap
        

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
        

        #self.init_variables()source /reg/g/psdm/etc/psconda.sh


       # print self.PiPiCo.shape, '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
               
        self.pos, self.colors = zip(*cmapToColormap(matplotlib.cm.jet))
        # Set the colormap
        self.clrmp =  pg.ColorMap(self.pos, self.colors)


        self.TofGui = TofGUI()
        self.TofGui.TofPlotWidget.scene().sigMouseMoved.connect(self.mouseMoved_Tof)
        self.TofGui.show()
                
        self.XYGui = XYGUI()                   
       # self.XYPlot = pg.ImageView(name='XY')
        self.XYGui.XYPlot.setColorMap(self.clrmp) 
        
        self.XYGui.XYPlot.view.invertY(False)
        
                       
        self.XYText = pg.LabelItem() 
        self.XYGui.XYPlot.addItem(self.XYText)
       # self.winXY.setCentralWidget(self.XYPlot)          
        self.XYGui.XYItem.scene().sigMouseMoved.connect(self.mouseMoved_XY)
        self.XYGui.show()
        
        self.XTGui = XTGUI()                   
       # self.XTPlot = pg.ImageView(name='XT')
        self.XTGui.XTPlot.setColorMap(self.clrmp)    
        
        self.XTGui.XTPlot.view.invertY(False)
                    
        self.XTText = pg.LabelItem() 
        self.XTGui.XTPlot.addItem(self.XTText)
       # self.winXT.setCentralWidget(self.XTPlot)          
        self.XTGui.XTItem.scene().sigMouseMoved.connect(self.mouseMoved_XT)
        self.XTGui.show()     
        
        self.YTGui = YTGUI()                   
       # self.YTPlot = pg.ImageView(name='YT')
        self.YTGui.YTPlot.setColorMap(self.clrmp) 
        
        self.YTGui.YTPlot.view.invertY(False)
                       
        self.YTTeYT = pg.LabelItem() 
        self.YTGui.YTPlot.addItem(self.YTTeYT)
       # self.winYT.setCentralWidget(self.YTPlot)          
        self.YTGui.YTItem.scene().sigMouseMoved.connect(self.mouseMoved_YT)
        self.YTGui.show()           
  
        self.PiPiCoGui = PiPiCoGUI()                   
       # self.PiPiCoPlot = pg.ImageView(name='PiPiCo')
        self.PiPiCoGui.PiPiCoPlot.setColorMap(self.clrmp)     
        
        self.PiPiCoGui.PiPiCoPlot.view.invertY(False)
                   
        self.PiPiCoTePiPiCo = pg.LabelItem() 
        self.PiPiCoGui.PiPiCoPlot.addItem(self.PiPiCoTePiPiCo)
       # self.winPiPiCo.setCentralWidget(self.PiPiCoPlot)          
        self.PiPiCoGui.PiPiCoItem.scene().sigMouseMoved.connect(self.mouseMoved_PiPiCo)
        self.PiPiCoGui.show()
        
        
        self.ctrlPanel = ControlPanel()
        
        self.ctrlPanel.ControlP.Clear.clicked.connect(self.ClearF)
        self.ctrlPanel.ControlP.SaveandClear.clicked.connect(self.SaveClearF)
        self.ctrlPanel.show()
        
        

                
        self.checkBoxes = [self.TofGui.TofUi.Gate1, self.TofGui.TofUi.Gate2, self.TofGui.TofUi.Gate3, self.XYGui.XYUi.RectGate, self.XYGui.XYUi.CircleGate1, self.XYGui.XYUi.CircleGate2, self.XTGui.XTUi.RectGate, self.XTGui.XTUi.CircleGate1, self.XTGui.XTUi.CircleGate2, self.YTGui.YTUi.RectGate, self.YTGui.YTUi.CircleGate1, self.YTGui.YTUi.CircleGate2,self.PiPiCoGui.PiPiCoUi.RectGate, self.PiPiCoGui.PiPiCoUi.CircleGate1, self.PiPiCoGui.PiPiCoUi.CircleGate2]
        self.ckbParents_a = [self.TofGui.TofCurve, self.TofGui.TofCurve, self.TofGui.TofCurve, self.XYGui.XYPlot.getImageItem(), self.XYGui.XYPlot.getImageItem(), self.XYGui.XYPlot.getImageItem(), self.XTGui.XTPlot.getImageItem(), self.XTGui.XTPlot.getImageItem(), self.XTGui.XTPlot.getImageItem(), self.YTGui.YTPlot.getImageItem(), self.YTGui.YTPlot.getImageItem(), self.YTGui.YTPlot.getImageItem(), self.PiPiCoGui.PiPiCoPlot.getImageItem(), self.PiPiCoGui.PiPiCoPlot.getImageItem(), self.PiPiCoGui.PiPiCoPlot.getImageItem()]
        self.ckbParents = [self.TofGui.TofPlotWidget, self.TofGui.TofPlotWidget, self.TofGui.TofPlotWidget, self.XYGui.XYItem.vb, self.XYGui.XYItem.vb, self.XYGui.XYItem.vb, self.XTGui.XTItem.vb, self.XTGui.XTItem.vb, self.XTGui.XTItem.vb, self.YTGui.YTItem.vb, self.YTGui.YTItem.vb, self.YTGui.YTItem.vb, self.PiPiCoGui.PiPiCoItem.vb, self.PiPiCoGui.PiPiCoItem.vb, self.PiPiCoGui.PiPiCoItem.vb]        
        self.ckbParents_b = [self.TofGui.TofPlotWidget, self.TofGui.TofPlotWidget, self.TofGui.TofPlotWidget, self.XYGui.XYItem, self.XYGui.XYItem, self.XYGui.XYItem, self.XYGui.XYItem, self.XTGui.XTItem, self.XTGui.XTItem, self.XTGui.XTItem, self.XTGui.XTItem, self.YTGui.YTItem, self.YTGui.YTItem, self.YTGui.YTItem, self.YTGui.YTItem, self.PiPiCoGui.PiPiCoItem, self.PiPiCoGui.PiPiCoItem, self.PiPiCoGui.PiPiCoItem, self.PiPiCoGui.PiPiCoItem]        
        self.num_ckBoxes = len(self.checkBoxes)
        
        self.init_variables()
        
        self.rois = [pg.LinearRegionItem([0,0]), pg.LinearRegionItem([0,0]), pg.LinearRegionItem([0,0]), pg.RectROI(pos=[0,0],size = [1,1]), pg.CircleROI(pos=[0,0],size = [1,1]), pg.CircleROI(pos=[0,0],size = [1,1]), pg.RectROI(pos=[0,0],size = [1,1]), pg.CircleROI(pos=[0,0],size = [1,1]), pg.CircleROI(pos=[0,0],size = [1,1]), pg.RectROI(pos=[0,0],size = [1,1]), pg.CircleROI(pos=[0,0],size = [1,1]), pg.CircleROI(pos=[0,0],size = [1,1]), pg.RectROI(pos=[0,0],size = [1,1]), pg.CircleROI(pos=[0,0],size = [1,1]), pg.CircleROI(pos=[0,0],size = [1,1])]
        self.roiTypes = ['Linear', 'Linear', 'Linear', 'Rect', 'Circle', 'Circle', 'Rect', 'Circle', 'Circle', 'Rect', 'Circle', 'Circle', 'Rect', 'Circle', 'Circle']
        self.roiNames = ['Gate1', 'Gate2', 'Gate3', 'Rect', 'Circle1', 'Circle2', 'Rect', 'Circle1', 'Circle2', 'Rect', 'Circle1', 'Circle2', 'Rect', 'Circle1', 'Circle2']
        self.colors = [QtGui.QColor(255,0,0,127),QtGui.QColor(0,255,0,127),QtGui.QColor(0,0,255,127),'r','g','k','r','g','k','r','g','k','r','g','k']
        #print 'len:',len(self.roiTypes), self.roiTypes[3]
        self.roiStates = [0]*self.num_ckBoxes
        
        self.count_labels = [self.TofGui.TofUi.Gate1Yield,self.TofGui.TofUi.Gate2Yield,self.TofGui.TofUi.Gate3Yield, self.XYGui.XYUi.RectYield, self.XYGui.XYUi.Circle1Yield, self.XYGui.XYUi.Circle2Yield, self.XTGui.XTUi.RectYield, self.XTGui.XTUi.Circle1Yield, self.XTGui.XTUi.Circle2Yield, self.YTGui.YTUi.RectYield, self.YTGui.YTUi.Circle1Yield, self.YTGui.YTUi.Circle2Yield, self.PiPiCoGui.PiPiCoUi.RectYield, self.PiPiCoGui.PiPiCoUi.Circle1Yield, self.PiPiCoGui.PiPiCoUi.Circle2Yield
]
        self.rate_labels = [self.TofGui.TofUi.Gate1Rate,self.TofGui.TofUi.Gate2Rate,self.TofGui.TofUi.Gate3Rate,self.XYGui.XYUi.RectRate, self.XYGui.XYUi.Circle1Rate, self.XYGui.XYUi.Circle2Rate,self.XTGui.XTUi.RectRate, self.XTGui.XTUi.Circle1Rate, self.XTGui.XTUi.Circle2Rate,self.YTGui.YTUi.RectRate, self.YTGui.YTUi.Circle1Rate, self.YTGui.YTUi.Circle2Rate,self.PiPiCoGui.PiPiCoUi.RectRate, self.PiPiCoGui.PiPiCoUi.Circle1Rate, self.PiPiCoGui.PiPiCoUi.Circle2Rate]
        
        self.total_count_labels = [self.TofGui.TofUi.TotalYield,self.XYGui.XYUi.TotalYield,self.XTGui.XTUi.TotalYield,self.YTGui.YTUi.TotalYield,self.PiPiCoGui.PiPiCoUi.TotalYield]
        self.total_rate_labels = [self.TofGui.TofUi.TotalRate,self.XYGui.XYUi.TotalRate,self.XTGui.XTUi.TotalRate,self.YTGui.YTUi.TotalRate,self.PiPiCoGui.PiPiCoUi.TotalRate]
        
        self.arrs = [0,0,0,self.XY, self.XY,self.XY,self.XT, self.XT,self.XT,self.YT, self.YT,self.YT,self.PiPiCo, self.PiPiCo,self.PiPiCo]
        
        
        
        self.old_counts = [0]*self.num_ckBoxes
        self.new_counts = [0]*self.num_ckBoxes
        self.num_shots = np.zeros(self.num_ckBoxes)
        
        self.num_evts = 120
        
        self.num_shot = 0
        self.old_count = 0
        self.new_count = 0

        self.total_num_shots = 0
        self.speed_rep_int = 120
        self.old_time = time.time()
        
        for i in range(self.num_ckBoxes):
            if self.roiTypes[i] == 'Linear':
           #     print 'a:',i, self.roiTypes[i]
                self.rois[i].sigRegionChanged.connect(lambda: self.sum_under_linear_roi(i))
                self.rois[i].sigRegionChanged.connect(lambda: self.disableMouse(self.ckbParents_b[i]))
                self.rois[i].sigRegionChangeFinished.connect(lambda: self.enableMouse(self.ckbParents_b[i]))
                self.rois[i].sigRegionChangeFinished.connect(lambda: self.reset_num_shots(i))
            else:
             #   print 'b:',i, self.roiTypes[i]
              #  self.rois[i].sigRegionChanged.connect(lambda: self.roiMoved(self.rois[i]))
                self.rois[i].sigRegionChanged.connect(lambda: self.sum_under_2d_roi(i))
                self.rois[i].sigRegionChangeStarted.connect(lambda: self.disableMouse(self.ckbParents_b[i]))
                self.rois[i].sigRegionChangeFinished.connect(lambda: self.enableMouse(self.ckbParents_b[i]))
                self.rois[i].sigRegionChangeFinished.connect(lambda: self.reset_num_shots(i))
                
                
        
        
        self.data_dict = {}
        self.local_data_dict = {}
        
        self.tof_inds = []
        

        self.zeromq_listener_thread = QtCore.QThread()

      
        self.zeromq_listener = ZMQListener(self.rec_ip, self.rec_port, u'coin_data')
        self.init_listening_thread()
        
        self.refresh_timer = QtCore.QTimer()
        self.init_timer()

      #  self.show()
      
      
    def init_variables(self):
        self.Xaxis  = np.linspace(self.Xmin, self.Xmax, self.Xbinnum)
        self.Yaxis = np.linspace(self.Ymin, self.Ymax, self.Ybinnum)
        self.Taxis = np.linspace(self.Tmin, self.Tmax, self.Tbinnum)
        
        self.Xaxis_r  = self.Xaxis[::-1]
        self.Yaxis_r = self.Yaxis[::-1]
        self.Taxis_r = self.Taxis[::-1]
 
        self.XaxisM = (self.Xaxis[:-1] + self.Xaxis[1:])/2
        self.YaxisM = (self.Yaxis[:-1] + self.Yaxis[1:])/2
        self.TaxisM = (self.Taxis[:-1] + self.Taxis[1:])/2
        
        self.XY = np.zeros([self.Xbinnum-1, self.Ybinnum-1])
        self.Tof = np.zeros([self.Tbinnum-1,1])
        self.XT = np.zeros([self.Tbinnum-1, self.Xbinnum-1])
        self.YT = np.zeros([self.Tbinnum-1, self.Ybinnum-1])
        self.TSumX = np.zeros([self.Tbinnum-1,1])
        self.TSumY = np.zeros([self.Tbinnum-1,1])
        
        self.PiPiCo = np.zeros([self.Tbinnum-2,self.Tbinnum-2])      
        
        self.num_total_shots = 0
        
        
        self.num_shots = np.zeros(self.num_ckBoxes)
        
        self.num_evts = 120
        
        self.num_shot = 0
        self.old_count = 0
        self.new_count = 0



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
        self.refresh_timer.start(5.0)

    def data_received(self, dat):
       # print 'data received'
        self.data_dict = copy.deepcopy(dat)
        
        self.total_num_shots += 1
                        
        self.tof_inds = []
        
        for newhit in self.data_dict['ion_hits']:            
       #     Tofind_l = np.where(self.Taxis >= self.newhit[0])[0][0]
       #     Xind_l = np.where(self.Xaxis >= self.newhit[1])[0][0]
       #     Yind_l = np.where(self.Yaxis >= self.newhit[2])[0][0]
            
            Tofind = next((Tof_ind for Tof_ind, Tof_ele in enumerate(self.Taxis) if Tof_ele > newhit[0]),0)
            Xind = next((X_ind for X_ind, X_ele in enumerate(self.Xaxis) if X_ele > newhit[1]),0)
            Yind = next((Y_ind for Y_ind, Y_ele in enumerate(self.Yaxis) if Y_ele > newhit[2]),0)
            
            self.tof_inds.append(Tofind-1)
            
            self.Tof[Tofind-1] += 1
            self.XY[Xind-1, Yind-1] += 1
            self.XT[Tofind-1, Xind-1] += 1
            self.YT[Tofind-1, Yind-1] += 1 
        
        self.tof_inds = sorted(self.tof_inds)    
        if len(self.tof_inds) > 1:
            for i_tof_ind in range(len(self.tof_inds)-1):
             #   print '****************************************',self.PiPiCo.shape, len(self.tof_inds)
                self.PiPiCo[self.tof_inds[i_tof_ind],self.tof_inds[(i_tof_ind+1):]]  += 1
           # print self.PiPiCo.shape
            
        self.data_dict = {}
        
        self.num_total_shots += 1
        self.num_shot += 1
        
        if self.num_shot == 1:
            self.old_count = np.sum(self.Tof)
        if self.num_shot == self.num_evts:
            self.new_count = np.sum(self.Tof)
            total_rate = (self.new_count - self.old_count)/self.num_evts
            for lb in self.total_rate_labels:
                lb.setText("TotalRate:%0.1f" % total_rate)
            self.num_shot = 0
            
        
        self.num_shots = self.num_shots + 1

        for i in range(self.num_ckBoxes):
         #   if self.roiStates[i] == 0:
         #       self.rate_labels[i].setText("< >")
            if self.roiStates[i] == 1:
                if self.num_shots[i] == 1:                    
                    if self.roiTypes[i] == 'Linear':
                       # print 'linear', self.num_shots[i]
                        self.old_counts[i] = self.sum_under_linear_roi(i)
                    else:
                        self.old_counts[i] = self.sum_under_2d_roi(i)
                if self.num_shots[i] == self.num_evts:

                    if self.roiTypes[i] == 'Linear':
                      #  print self.num_shots[i]
                        self.new_counts[i] = self.sum_under_linear_roi(i)
                        rate_l = (self.new_counts[i]-self.old_counts[i])/self.num_evts
                        self.rate_labels[i].setText("R:%0.1f" % rate_l)
                        self.num_shots[i] = 0
                        print 'linear:', rate_l, i
                    else:
                        self.new_counts[i] = self.sum_under_2d_roi(i)  
                        rate_2d = (self.new_counts[i]-self.old_counts[i])/self.num_evts
                        self.rate_labels[i].setText(self.roiNames[i]+"Rate:%0.1f" % rate_2d)
                        print '2d:', rate_2d, i
                        self.num_shots[i] = 0
                                  
            

    def update_images(self):
    
       # QtGui.QApplication.processEvents()
        
        self.TofGui.TofCurve.setData(np.squeeze(self.TaxisM),np.squeeze(self.Tof))
        
        self.max_XY = self.XY.max()
        self.XY_norm = self.XY
     #   pos_XY = np.array([0.0, max_XY/2, max_XY])
     #   color_XY = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XY = pg.ColorMap(pos_XY, color_XY)  
     #   self.XYPlot.setColorMap(clrmp_XY)           
        if self.max_XY != 0:  
            self.XY_norm = self.XY/self.max_XY   
            self.XYGui.XYPlot.setImage(self.XY_norm, autoRange = False, pos = [self.Xmin, self.Ymin], scale = [self.Xbin, self.Ybin])
            
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
        
        self.max_YT = self.YT.max()
     #   pos_YT = np.array([0.0, max_YT/2, max_YT])
     #   color_YT = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_YT = pg.ColorMap(pos_YT, color_YT)
     #   self.YTPlot.setColorMap(clrmp_YT)  
        if self.max_YT != 0:         
            self.YTGui.YTPlot.setImage(self.YT/self.max_YT, autoRange = False, pos = [self.Tmin, self.Ymin], scale = [self.Tbin, self.Ybin])
            self.YTGui.YTItem.setAspectLocked(False)
            
        self.max_PiPiCo = self.PiPiCo.max()
     #   pos_PiPiCo = np.array([0.0, max_PiPiCo/2, max_PiPiCo])
     #   color_PiPiCo = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubPiPiCoe)
     #   clrmp_PiPiCo = pg.ColorMap(pos_PiPiCo, color_PiPiCo)
     #   self.PiPiCoPlot.setColorMap(clrmp_PiPiCo)  
        if self.max_PiPiCo != 0:         
            self.PiPiCoGui.PiPiCoPlot.setImage(self.PiPiCo/self.max_PiPiCo, autoRange = False, pos = [self.Tmin, self.Tmin], scale = [self.Tbin, self.Tbin])
            self.PiPiCoGui.PiPiCoItem.setAspectLocked(False)     
            
            
        if self.total_num_shots % self.speed_rep_int == 0:
            self.time = time.time()
            print('Processed: {0} in {1:.2f} seconds ({2:.2f} Hz)'.format(
                self.total_num_shots,
                self.time - self.old_time,
                float(self.speed_rep_int)/float(self.time-self.old_time)))
            sys.stdout.flush()
            self.old_time = self.time           
            
        self.check_checkBox()
        self.update_numbers()
  #      print np.sum(self.Tof), np.sum(self.XY)
        for lb in self.total_count_labels:
            lb.setText("TotalYield:%0.1f" % np.sum(self.XY))
        
    def reset_num_shots(self,i):
        self.num_shots[i] = 0
        
    def update_numbers(self):
        for i in range(self.num_ckBoxes):
            if self.roiStates[i] != 0:
                if self.roiTypes[i] == 'Linear':
                 #   print 'i1:',i
                    self.sum_under_linear_roi(i)
                
                else:
                    self.sum_under_2d_roi(i)

            
    def check_checkBox(self):
        for i in range(self.num_ckBoxes):
        
            if self.checkBoxes[i].isChecked() and self.roiStates[i] == 0:
                
                
                xmin, xmax = self.ckbParents_b[i].getAxis('bottom').range
                ymin, ymax = self.ckbParents_b[i].getAxis('left').range
              #  print xmin, ymax, type(ymax)
                if self.roiTypes[i] == 'Linear':
                    self.rois[i].setRegion([xmin/10, xmax/10])
                   # self.rois[i].setZValue(-20)
                    self.rois[i].setBrush(color = self.colors[i])
                    self.ckbParents[i].addItem(self.rois[i])
                    self.roiStates[i] = 1
                 #   print 'i4:',i
                    self.num_shots[i] = 0
                    self.sum_under_linear_roi(i)
                    
                else:
                    self.rois[i].setPos([(xmin+xmax)/2, (ymin+ymax)/2])
                    self.rois[i].setSize([(xmax-xmin)/10, (ymax-ymin)/10])
                    self.rois[i].setPen(width=2.5,color=self.colors[i])
                    self.ckbParents[i].addItem(self.rois[i])
                    self.roiStates[i] = 1   
                    
                    self.num_shots[i] = 0         
                 #   print 'i5:',i       
                    self.sum_under_2d_roi(i)

                   
                
            if not self.checkBoxes[i].isChecked() and self.roiStates[i] == 1:
                self.ckbParents[i].removeItem(self.rois[i])
                self.roiStates[i] = 0
                
    def sum_under_linear_roi(self, i):
       # print 'sum_linear i:',i
        if self.roiStates[i] == 0 or self.roiTypes[i] != 'Linear':
            return
        x1, x2 = self.rois[i].getRegion()
        Tofind1 = next((Tof_ind for Tof_ind, Tof_ele in enumerate(self.Taxis) if Tof_ele > x1),None) 
        Tofind2 = next((Tof_ind for Tof_ind, Tof_ele in enumerate(self.Taxis) if Tof_ele > x2),None) 
        
        if Tofind1 is None or Tofind2 is None:
            return
            
        Tofind1 -= 1
        Tofind2 -= 1         
        roi_yield = np.sum(self.Tof[Tofind1:Tofind2])
        r_roi_yield = roi_yield
        #return self.TaxisM[Tofind1], self.TaxisM[Tofind2], np.sum(self.Tof[Tofind1:Tofind2])
        self.count_labels[i].setText(self.roiNames[i]+"Yield:%0.1f" % roi_yield)
        return r_roi_yield

        
    def sum_under_2d_roi(self, i):
      #  print 'sum_2d i:',i
        if self.roiStates[i] == 0:
            return
        arr = self.rois[i].getArrayRegion(self.arrs[i], self.ckbParents_a[i])
        
        roi_yield = np.sum(np.sum(arr))
        r_roi_yield = roi_yield
        #print 'ROI yield:',roi_yield, coords_border_y_x1, coords_border_y_x2
       # return np.sum(np.sum(arr))*scale_arr, coords_border_y_x1, coords_border_y_x2
        self.count_labels[i].setText(self.roiNames[i]+"Yield:%0.1f" % roi_yield)

    
        return r_roi_yield
                     
                
    def disableMouse(self, prts):
        prts.setMouseEnabled(x=False, y=False)
     #   print 'disable', prts, prts.getAxis('bottom').range
        
    def enableMouse(self, prts):
        prts.setMouseEnabled(x=True, y=True)
     #   print 'enable'    
            
            
      #  QtGui.QApplication.processEvents()
        

    def start_gui():
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app = QtGui.QApplication(sys.argv)
        #print 'sys.arv:',len(sys.argv)


        rec_ip = '172.21.50.21'
        rec_port = 12321

        _ = MainFrame(rec_ip, rec_port)
        sys.exit(app.exec_())
        
    def mouseMoved_Tof(self,pos):
        #print "X, Y:", self.
        mousePoint = self.TofGui.TofCurve.mapFromScene(pos)
        #mousePoint = self.TofGui.TofCurve.mapSceneToItem(pos)
        self.TofGui.TofUi.MousePosition.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))        
        
    def mouseMoved_XY(self,pos):
        #print "X, Y:", self.
        #mousePoint = self.XYItem.mapFromScene(pos)
        mousePoint = self.XYGui.XYItem.vb.mapSceneToView(pos)
        self.XYGui.XYUi.MousePosition.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))
        
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
                
        
    def roiMoved(self,roi):
        #print "X, Y:", self.
        #mousePoint = self.XYItem.mapFromScene(pos)
        #mousePoint = self.XYGui.XYItem.vb.mapSceneToView(roi.pos())
        
        #self.XYGui.XYUi.label_2.setText("x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y()))
        self.XYGui.XYUi.label_2.setText("x=%0.1f,y=%0.1f" % (roi.pos()[0],roi.pos()[1]))
    #    print 'size of roi:',roi.size()
    
    
    def ClearF(self):
        self.init_variables()
        
    def SaveClearF(self):
        h5file = h5py.File('data.h5','w')
        h5file.create_dataset('Tof',data=self.Tof/self.num_total_shots)
        h5file.create_dataset('XY',data=self.XY/self.num_total_shots)
        h5file.create_dataset('XT',data=self.XT/self.num_total_shots)
        h5file.create_dataset('YT',data=self.YT/self.num_total_shots)    
        h5file.create_dataset('PiPiCo',data=self.PiPiCo/self.num_total_shots)
        h5file.close()
        
        self.init_variables()




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
        sys.exit()

    _ = MainFrame(rec_ip, rec_port)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
