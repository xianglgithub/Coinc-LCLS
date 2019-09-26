

import sys
import numpy as np
import signal
import datetime
import copy
import pyqtgraph as pg
import matplotlib
from pyqtgraph.Qt import QtGui, QtCore

import XY1GatedPlots, XY1GatedTof
#from GUIs import XYGPlots1, XYGTof1

from cmapToColormap import cmapToColormap                        

class GateXY1():
    def __init__(self,parent):
         
        
        self.parent = parent
      
        self.tof_inds = []
        
        self.roi =  pg.RectROI(pos=[0,0],size = [1,1])
        self.roiState = 0
        
        self.roi.sigRegionChanged.connect(lambda: self.sum_under_2d_roi())
        self.roi.sigRegionChangeStarted.connect(lambda: self.disableMouse())
        self.roi.sigRegionChangeFinished.connect(lambda: self.enableMouse())
        self.roi.sigRegionChangeFinished.connect(lambda: self.gate_move_finished())

        
        self.roiName = 'RectGate1'
        #self.num_shots = 0
        
        self.initialize_variables()
        
        self.initialize_plots()
        

        
    def sum_under_2d_roi(self):
      #  print 'sum_2d i:',i
        if self.roiState == 0:
            return
        arr = self.roi.getArrayRegion(self.parent.XY, self.parent.XYPlot.getImageItem())
        
        roi_yield = np.sum(np.sum(arr))
       # r_roi_yield = roi_yield
        #print 'ROI yield:',roi_yield, coords_border_y_x1, coords_border_y_x2
       # return np.sum(np.sum(arr))*scale_arr, coords_border_y_x1, coords_border_y_x2
        self.parent.XYUi.Rect1Yield.setText(self.roiName+"Yield:%0.1f" % roi_yield)
    
        return roi_yield         
        
   
        
    def disableMouse(self):
        self.parent.XYItem.setMouseEnabled(x=False, y=False)
     #   print 'disable', prts, prts.getAxis('bottom').range
     

        
    def enableMouse(self):
        self.parent.XYItem.setMouseEnabled(x=True, y=True)
        
         
    def update_variables(self, Tofind, Xind, Yind, eXInd, eYInd):
     
     #change here Xind to X(Xind)
        if self.Xaxis[Xind] > self.x_cond_s and self.Xaxis[Xind] < self.x_cond_l and self.Yaxis[Yind] > self.y_cond_s and self.Yaxis[Yind] < self.y_cond_l:             
            self.tof_inds.append(Tofind-1)           
            self.Tof[Tofind-1] += 1
            self.XT[Tofind-1, Xind-1] += 1
            self.YT[Tofind-1, Yind-1] += 1   
            
    def update_PiPiCo(self):
        self.tof_inds = sorted(self.tof_inds)
        if len(self.tof_inds) > 1:
           for i_tof_ind in range(len(self.tof_inds)-1):
             #   print '****************************************',self.PiPiCo.shape, len(self.tof_inds)
               self.PiPiCo[self.tof_inds[i_tof_ind],self.tof_inds[(i_tof_ind+1):]]  += 1
           # print self.PiPiCo.shape     
           self.tof_inds = []
           
    def gate_move_finished(self):
        print 'gate moved'
        self.initialize_variables()      
        print self.roi.pos(), self.roi.size() 
        

        self.x_cond_s = self.roi.pos()[0]
        self.x_cond_l = self.roi.pos()[0] +  self.roi.size()[0]
        self.y_cond_s = self.roi.pos()[1]
        self.y_cond_l = self.roi.pos()[1] + self.roi.size()[1]
        
#        self.XYG_ind1 = np.array([(self.Xaxis>self.x_cond_s) & (self.Xaxis<self.x_cond_l)], dtype= np.bool)
        self.XYG_ind1 = (self.XaxisM>self.x_cond_s) & (self.XaxisM<self.x_cond_l)
        #self.XYG_ind1 = self.XYG_ind1[:,np.newaxis]
        print '******************************************************************************',type(self.XYG_ind1)

        self.XYG_ind2 = (self.YaxisM>self.y_cond_s) & (self.YaxisM<self.y_cond_l)
        #self.XYG_ind2 = self.XYG_ind2[np.newaxis,:]
  #      self.XYG = np.zeros((self.XYG_ind1,len(self.XYG_ind2)))     
     #   self.XYG_ind = self.XYG_ind1 & self.XYG_ind2
     #   print '******************************************************************************',self.XYG_ind.shape
        
    def initialize_variables(self):
    
       
        self.shot_num = 0
        self.old_count = 0
        self.new_count = 0    
                     
        self.XYG = np.zeros([self.Xbinnum-1, self.Ybinnum-1])
        self.Tof = np.zeros([self.Tbinnum-1,1])
        self.XT = np.zeros([self.Tbinnum-1, self.Xbinnum-1])
        self.YT = np.zeros([self.Tbinnum-1, self.Ybinnum-1])
#        self.TSumX = np.zeros([self.Tbinnum-1,1])
 #       self.TSumY = np.zeros([self.Tbinnum-1,1])
#        self.X_arr  = np.arange(len(self.Xbinnum-1))
 #       self.Y_arr  = np.arange(len(self.Ybinnum-1))
        self.PiPiCo = np.zeros([self.Tbinnum-2,self.Tbinnum-2])  
        
       # self.XYG_ind1 = np.array([],dtype=np.bool)
       # self.XYG_ind2 = np.array([],dtype=np.bool)
        
       # print 'XYG shape1:', self.XYG.shape
#        print self.XYG_ind1, self.XYG_ind2 
        
        
    def initialize_plots(self):
         
        self.plotWindow = XYGPlots1()   
        self.tofWindow = XYGTof1()           
        
    def update_plots(self):
    
       # QtGui.QApplication.processEvents()
        
        self.tofWindow.TofCurve.setData(np.squeeze(self.TaxisM),np.squeeze(self.Tof))
        
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
      #  print self.x_cond_s, self.x_cond_l, self.y_cond_s, self.y_cond_l, self.XYG.shape, self.XYG_ind1.shape,self.XYG_ind2.shape, self.parent.XY.shape
        print self.parent.XY.shape
        #self.XYG = self.parent.XY[self.XYG_ind1, self.XYG_ind2]
        print '&&&&&&&&&&&&&&&&&&&', self.XYG.shape
        self.XYG = self.parent.XY[np.ix_(self.XYG_ind1,self.XYG_ind2)]
        if self.XYG.shape[0] > 0:
            self.max_XYG = self.XYG.max()
            self.XYG_norm = self.XYG
     #   pos_XY = np.array([0.0, max_XY/2, max_XY])
     #   color_XY = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XY = pg.ColorMap(pos_XY, color_XY)  
     #   self.XYPlot.setColorMap(clrmp_XY)           
            if self.max_XYG != 0:  
                print 'xy: true'
                self.XYG_norm = self.XYG/self.max_XYG   
                self.plotWindow.XYPlot.setImage(self.XYG_norm, autoRange = False, pos = [self.x_cond_s, self.y_cond_s], scale = [self.Xbin, self.Ybin])
            
        #    self.tr = self.coord_transform(self.XY, self.XYGui.XYPlot.getImageItem(), axes=(0,1))
            #self.XYItem.setAspectLocked(False)
            #self.XYPlot.setImage(self.XY/max_XY, autoRange = False)
        
        self.max_XT = self.XT.max()
     #   pos_XT = np.array([0.0, max_XT/2, max_XT])
     #   color_XT = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XT = pg.ColorMap(pos_XY, color_XT)  
     #   self.XTPlot.setColorMap(clrmp_XT)   
        if self.max_XT != 0:                            
            self.plotWindow.XTPlot.setImage(self.XT/self.max_XT, autoRange = False, pos = [self.Tmin, self.Xmin], scale = [self.Tbin, self.Xbin])
            self.plotWindow.XTItem.setAspectLocked(False)
        
        self.max_YT = self.YT.max()
     #   pos_YT = np.array([0.0, max_YT/2, max_YT])
     #   color_YT = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_YT = pg.ColorMap(pos_YT, color_YT)
     #   self.YTPlot.setColorMap(clrmp_YT)  
        if self.max_YT != 0:         
            self.plotWindow.YTPlot.setImage(self.YT/self.max_YT, autoRange = False, pos = [self.Tmin, self.Ymin], scale = [self.Tbin, self.Ybin])
            self.plotWindow.YTItem.setAspectLocked(False)
            
        self.max_PiPiCo = self.PiPiCo.max()
     #   pos_PiPiCo = np.array([0.0, max_PiPiCo/2, max_PiPiCo])
     #   color_PiPiCo = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubPiPiCoe)
     #   clrmp_PiPiCo = pg.ColorMap(pos_PiPiCo, color_PiPiCo)
     #   self.PiPiCoPlot.setColorMap(clrmp_PiPiCo)  
        if self.max_PiPiCo != 0:         
            self.plotWindow.PiPiCoPlot1.setImage(self.PiPiCo/self.max_PiPiCo, autoRange = False, pos = [self.Tmin, self.Tmin], scale = [self.Tbin, self.Tbin])
            self.plotWindow.PiPiCoItem1.setAspectLocked(False)            
            
            self.plotWindow.PiPiCoPlot2.setImage(self.PiPiCo/self.max_PiPiCo, autoRange = False, pos = [self.Tmin, self.Tmin], scale = [self.Tbin, self.Tbin])
            self.plotWindow.PiPiCoItem2.setAspectLocked(False)            



class XYGTof1(QtGui.QMainWindow):
    def __init__(self, parent=None):

        super(XYGTof1, self).__init__()
        
        
        self.XYGTofUi = XY1GatedTof.Ui_XY1GatedTof()
        self.XYGTofUi.setupUi(self)
        
  
        self.TofPlotWidget= pg.PlotWidget()
        self.XYGTofUi.horizontalLayout.insertWidget(0, self.TofPlotWidget)
        self.TofCurve = self.TofPlotWidget.plot(pen='w')
        self.TofPlotWidget.setLabel('left', 'Yield')# units='A')
        self.TofPlotWidget.setLabel('bottom', 'Tof (ns)')         
        
        self.show()


            
class XYGPlots1(QtGui.QMainWindow):
    def __init__(self, parent=None):

        super(XYGPlots1, self).__init__()
        
        self.pos, self.colors = zip(*cmapToColormap(matplotlib.cm.jet))
        # Set the colormap
        self.clrmp =  pg.ColorMap(self.pos, self.colors)
        
        self.XYGPlotsUi = XY1GatedPlots.Ui_XY1GatedPlots()
        self.XYGPlotsUi.setupUi(self)
        
       # self.XYGPlotsUi.centralwidget.setColumnStrech(0,1)
        
        self.PiPiCoItem1 = pg.PlotItem(title = 'PiPiCo1',labels={'bottom': ('T', 'ns'), 'left': ('T', 'ns')})
        self.PiPiCoItem1.setAspectLocked(False)                      
        self.PiPiCoPlot1 = pg.ImageView(name='PiPiCo1', view=self.PiPiCoItem1) 
        self.PiPiCoPlot1.setColorMap(self.clrmp)                 
        self.XYGPlotsUi.Tof.insertWidget(0, self.PiPiCoPlot1)   

        
        self.XYItem = pg.PlotItem(title = 'XY',labels={'bottom': ('X', 'mm'), 'left': ('Y', 'mm')})
        self.XYItem.setAspectLocked(False)
        self.XYPlot = pg.ImageView(name='XY', view=self.XYItem) 
        self.XYPlot.setColorMap(self.clrmp) 
        self.XYGPlotsUi.XY.insertWidget(0, self.XYPlot)
        
        self.XTItem = pg.PlotItem(title = 'XT',labels={'bottom': ('T', 'ns'), 'left': ('X', 'mm')})
        self.XTItem.setAspectLocked(False)
        self.XTPlot = pg.ImageView(name='XT', view=self.XTItem) 
        self.XTPlot.setColorMap(self.clrmp)         
        self.XYGPlotsUi.XT.insertWidget(0, self.XTPlot)
        
        self.YTItem = pg.PlotItem(title = 'YT',labels={'bottom': ('T', 'ns'), 'left': ('Y', 'mm')})
        self.YTItem.setAspectLocked(False)
        self.YTPlot = pg.ImageView(name='YT', view=self.YTItem) 
        self.YTPlot.setColorMap(self.clrmp)         
        self.XYGPlotsUi.YT.insertWidget(0, self.YTPlot)       
        
        
        self.PiPiCoItem2 = pg.PlotItem(title = 'PiPiCo2',labels={'bottom': ('T', 'ns'), 'left': ('T', 'ns')})
        self.PiPiCoItem2.setAspectLocked(False)                      
        self.PiPiCoPlot2 = pg.ImageView(name='PiPiCo2', view=self.PiPiCoItem2) 
        self.PiPiCoPlot2.setColorMap(self.clrmp)                 
        self.XYGPlotsUi.PiPiCo.insertWidget(0, self.PiPiCoPlot2)  
        
        
        self.eXYItem = pg.PlotItem(title = 'eXY',labels={'bottom': ('X', 'mm'), 'left': ('Y', 'mm')})
        self.eXYItem.setAspectLocked(False)
        self.eXYPlot = pg.ImageView(name='eXY', view=self.eXYItem) 
        self.eXYPlot.setColorMap(self.clrmp)         
        self.XYGPlotsUi.eXY.insertWidget(0, self.eXYPlot)
        
        self.show()
        

