

import sys
import numpy as np
import signal
import datetime
import copy
import pyqtgraph as pg
import matplotlib
from pyqtgraph.Qt import QtGui, QtCore

import PiPiCo1GatedPlots, PiPiCo1GatedPlots1D
#from UI.GUIs import PiPiCoGPlots1, PiPiCoGPlots1D1
from cmapToColormap import cmapToColormap                        

class GatePiPiCo1():
    def __init__(self,parent):
         
        
        self.parent = parent                                                      
        
        self.tof_inds1 = []
        self.tof_inds2 = []
        
        self.roi =  pg.RectROI(pos=[0,0],size = [1,1])
   #     self.roiState = 0
        
        self.roi.sigRegionChangeFinished.connect(lambda: self.sum_under_2d_roi())
        self.roi.sigRegionChangeStarted.connect(lambda: self.disableMouse())
        self.roi.sigRegionChangeFinished.connect(lambda: self.enableMouse())
        self.roi.sigRegionChangeFinished.connect(lambda: self.gate_move_finished())

        
        self.roiName = 'RectGate1'
        self.num_shots = 0
        
        self.initialize_variables()
        
        self.initialize_plots()
        
        self.P1 = 0
        self.P2 = 0
        self.P12 = 0
        

        
    def sum_under_2d_roi(self):
      #  print 'sum_2d i:',i
        if self.parent.RectGate1_roiState== 0:
            return 0
        arr = self.roi.getArrayRegion(self.parent.PiPiCo, self.parent.PiPiCoPlot.getImageItem())
        
        roi_yield = np.sum(np.sum(arr))
       # r_roi_yield = roi_yield
        #print 'ROI yield:',roi_yield, coords_border_y_x1, coords_border_y_x2
       # return np.sum(np.sum(arr))*scale_arr, coords_border_y_x1, coords_border_y_x2
        self.parent.PiPiCoUi.Rect1Yield.setText(self.roiName+"Yield:%0.1f" % roi_yield)
    
        return roi_yield         
        
   
        
    def disableMouse(self):
        self.parent.PiPiCoItem.setMouseEnabled(x=False, y=False)
     #   print 'disable', prts, prts.getAxis('bottom').range
     

        
    def enableMouse(self):
        self.parent.PiPiCoItem.setMouseEnabled(x=True, y=True)
        
         
    def update_variables(self, Tofind):
     
     #change here Xind to X(Xind)
        if (self.parent.prt.Taxis[Tofind] > self.x_cond_s and self.parent.prt.Taxis[Tofind] < self.x_cond_l):             
          #  self.tof_inds1.append(Tofind-1) 
          #  self.x_inds1.append(Xind-1)  
          #  self.y_inds1.append(Yind-1)  
            self.P1 += 1
        if (self.parent.prt.Taxis[Tofind] > self.y_cond_s and self.parent.prt.Taxis[Tofind] < self.y_cond_l):
           # self.tof_inds2.append(Tofind-1)
           # self.x_inds2.append(Xind-1)  
           # self.y_inds2.append(Yind-1)             
            
           # self.XY[Xind-1, Yind-1] += 1
           # self.XT[Tofind-1, Xind-1] += 1
           # self.YT[Tofind-1, Yind-1] += 1   
            self.P2 += 1
            
        if (self.parent.prt.Taxis[Tofind] > self.x_cond_s and self.parent.prt.Taxis[Tofind] < self.x_cond_l) and (self.parent.prt.Taxis[Tofind] > self.y_cond_s and self.parent.prt.Taxis[Tofind] < self.y_cond_l):
           # self.tof_inds2.append(Tofind-1)
           # self.x_inds2.append(Xind-1)  
           # self.y_inds2.append(Yind-1)             
            
           # self.XY[Xind-1, Yind-1] += 1
           # self.XT[Tofind-1, Xind-1] += 1
           # self.YT[Tofind-1, Yind-1] += 1   
            self.P12 += 1 
            
    def coin(self):
    
        return (self.P1 > 0 and self.P2 > 0 and self.P12 == 0) or self.P12 > 1               
            
    def update_electron(self, eAind, eRind, eXind, eYind):
        
        self.eA[eAind,0] += 1            
        self.eR[eRind,0] += 1
        self.eXY[eXind, eYind] += 1
        self.eAR[eAind, eRind] += 1
        
    def reset_coin_var(self):
            
        self.P1 = 0
        self.P2 = 0
        self.P12 = 0
           
    def gate_move_finished(self):
        print 'gate moved'
        self.initialize_variables()      
        print self.roi.pos(), self.roi.size() 
        

        self.x_cond_s = self.roi.pos()[0]
        self.x_cond_l = self.roi.pos()[0] +  self.roi.size()[0]
        self.y_cond_s = self.roi.pos()[1]
        self.y_cond_l = self.roi.pos()[1] + self.roi.size()[1]
        
#        self.XYG_ind1 = np.array([(self.Xaxis>self.x_cond_s) & (self.Xaxis<self.x_cond_l)], dtype= np.bool)
        self.PiPiCoG_ind1 = (self.parent.prt.TaxisM>self.x_cond_s) & (self.parent.prt.TaxisM<self.x_cond_l)
        #self.XYG_ind1 = self.XYG_ind1[:,np.newaxis]
        #print '******************************************************************************',type(self.XYG_ind1)

        self.PiPiCoG_ind2 = (self.parent.prt.TaxisM>self.y_cond_s) & (self.parent.prt.TaxisM<self.y_cond_l)
        #self.XYG_ind2 = self.XYG_ind2[np.newaxis,:]
  #      self.XYG = np.zeros((self.XYG_ind1,len(self.XYG_ind2)))     
     #   self.XYG_ind = self.XYG_ind1 & self.XYG_ind2
     #   print '******************************************************************************',self.XYG_ind.shape
        
    def initialize_variables(self):
    
       
        self.shot_num = 0
        self.old_count = 0
        self.new_count = 0    
                     
        self.XY = np.zeros([self.parent.prt.Xbinnum-1, self.parent.prt.Ybinnum-1])
        
        self.eA = np.zeros([self.parent.prt.eAbinnum-1,1])
        self.eR = np.zeros([self.parent.prt.eRbinnum-1,1])      
        self.eAR = np.zeros([self.parent.prt.eAbinnum-1, self.parent.prt.eRbinnum-1])       
        self.eXY = np.zeros([self.parent.prt.eXbinnum-1, self.parent.prt.eYbinnum-1])      
               
        self.XT = np.zeros([self.parent.prt.Tbinnum-1, self.parent.prt.Xbinnum-1])
        self.YT = np.zeros([self.parent.prt.Tbinnum-1, self.parent.prt.Ybinnum-1])
#        self.TSumX = np.zeros([self.Tbinnum-1,1])
 #       self.TSumY = np.zeros([self.Tbinnum-1,1])
#        self.X_arr  = np.arange(len(self.Xbinnum-1))
 #       self.Y_arr  = np.arange(len(self.Ybinnum-1))
        self.PiPiCoG = np.zeros([self.parent.prt.Tbinnum-2,self.parent.prt.Tbinnum-2])  
        
       # self.XYG_ind1 = np.array([],dtype=np.bool)
       # self.XYG_ind2 = np.array([],dtype=np.bool)
        
       # print 'XYG shape1:', self.XYG.shape
#        print self.XYG_ind1, self.XYG_ind2 
        
        
    def initialize_plots(self):
         
        self.plotWindow = PiPiCoGPlots1()   
        self.plot1dWindow = PiPiCoGPlots1D1()           
        
    def update_plots(self):
    
        self.sum_under_2d_roi()
        
        self.plot1dWindow.Plots1DCurve.setData(np.squeeze(self.parent.prt.eAaxisM),np.squeeze(self.eA))
        self.plot1dWindow.Plots1DCurve1.setData(np.squeeze(self.parent.prt.eRaxisM),np.squeeze(self.eR))        
     #   print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
      #  print self.x_cond_s, self.x_cond_l, self.y_cond_s, self.y_cond_l, self.XYG.shape, self.XYG_ind1.shape,self.XYG_ind2.shape, self.parent.XY.shape

        #self.XYG = self.parent.XY[self.XYG_ind1, self.XYG_ind2]

        self.PiPiCoG = self.parent.PiPiCo[np.ix_(self.PiPiCoG_ind1,self.PiPiCoG_ind2)]
        if self.PiPiCoG.shape[0] > 0:
            self.max_PiPiCoG = self.PiPiCoG.max()
            self.PiPiCoG_norm = self.PiPiCoG
     #   pos_XY = np.array([0.0, max_XY/2, max_XY])
     #   color_XY = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XY = pg.ColorMap(pos_XY, color_XY)  
     #   self.XYPlot.setColorMap(clrmp_XY)           
            if self.max_PiPiCoG == 0:  
              #  print 'xy: true'
                self.max_PiPiCoG = 1
            self.PiPiCoG_norm = self.PiPiCoG/self.max_PiPiCoG   
            self.plotWindow.PiPiCoPlot.setImage(self.PiPiCoG_norm, autoRange = False, pos = [self.x_cond_s, self.y_cond_s], scale = [self.parent.prt.Tbin, self.parent.prt.Tbin])
            
        #    self.tr = self.coord_transform(self.XY, self.XYGui.XYPlot.getImageItem(), axes=(0,1))
            #self.XYItem.setAspectLocked(False)
            #self.XYPlot.setImage(self.XY/max_XY, autoRange = False)
        
        self.max_XT = self.XT.max()
     #   pos_XT = np.array([0.0, max_XT/2, max_XT])
     #   color_XT = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XT = pg.ColorMap(pos_XY, color_XT)  
     #   self.XTPlot.setColorMap(clrmp_XT)   
        if self.max_XT == 0:        
            self.max_XT = 1                    
        self.plotWindow.XTPlot.setImage(self.XT/self.max_XT, autoRange = False, pos = [self.parent.prt.Tmin, self.parent.prt.Xmin], scale = [self.parent.prt.Tbin, self.parent.prt.Xbin])
        self.plotWindow.XTItem.setAspectLocked(False)
        
        self.max_YT = self.YT.max()
     #   pos_YT = np.array([0.0, max_YT/2, max_YT])
     #   color_YT = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_YT = pg.ColorMap(pos_YT, color_YT)
     #   self.YTPlot.setColorMap(clrmp_YT)  
        if self.max_YT == 0:    
            self.max_YT = 1     
        self.plotWindow.YTPlot.setImage(self.YT/self.max_YT, autoRange = False, pos = [self.parent.prt.Tmin, self.parent.prt.Ymin], scale = [self.parent.prt.Tbin, self.parent.prt.Ybin])
        self.plotWindow.YTItem.setAspectLocked(False)
            
   #     self.max_PiPiCo = self.PiPiCo.max()
     #   pos_PiPiCo = np.array([0.0, max_PiPiCo/2, max_PiPiCo])
     #   color_PiPiCo = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubPiPiCoe)
     #   clrmp_PiPiCo = pg.ColorMap(pos_PiPiCo, color_PiPiCo)
     #   self.PiPiCoPlot.setColorMap(clrmp_PiPiCo)  

        self.max_XY = self.XY.max()
        self.XY_norm = self.XY
     #   pos_XY = np.array([0.0, max_XY/2, max_XY])
     #   color_XY = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XY = pg.ColorMap(pos_XY, color_XY)  
     #   self.XYPlot.setColorMap(clrmp_XY)           
        if self.max_XY == 0:  
          #  print 'xy: true'
            self.max_XY = 1
        self.XY_norm = self.XY/self.max_XY   
        self.plotWindow.XYPlot.setImage(self.XY_norm, autoRange = False, pos = [self.parent.prt.Xmin, self.parent.prt.Ymin], scale = [self.parent.prt.Xbin, self.parent.prt.Ybin])
            
        self.max_eXY = self.eXY.max()
        self.eXY_norm = self.eXY
     #   pos_XY = np.array([0.0, max_XY/2, max_XY])
     #   color_XY = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XY = pg.ColorMap(pos_XY, color_XY)  
     #   self.XYPlot.setColorMap(clrmp_XY)           
        if self.max_eXY == 0:  
         #   print 'xy: true'
            self.max_eXY = 1
        self.eXY_norm = self.eXY/self.max_eXY   
        self.plotWindow.eXYPlot.setImage(self.eXY_norm, autoRange = False, pos = [self.parent.prt.eXmin, self.parent.prt.eYmin], scale = [self.parent.prt.eXbin, self.parent.prt.eYbin])     
            
        self.max_eAR = self.eAR.max()
        self.eAR_norm = self.eAR
     #   pos_XY = np.array([0.0, max_XY/2, max_XY])
     #   color_XY = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XY = pg.ColorMap(pos_XY, color_XY)  
     #   self.XYPlot.setColorMap(clrmp_XY)           
        if self.max_eAR == 0:  
         #   print 'xy: true'
            self.max_eAR = 1
        self.eAR_norm = self.eAR/self.max_eAR   
        self.plotWindow.eARPlot.setImage(self.eAR_norm, autoRange = False, pos = [self.parent.prt.eAmin, self.parent.prt.eRmin], scale = [self.parent.prt.eAbin, self.parent.prt.eRbin])                              
                                 



class PiPiCoGPlots1D1(QtGui.QMainWindow):
    def __init__(self, parent=None):

        super(PiPiCoGPlots1D1, self).__init__()
        
        
        self.PiPiCoGPlots1DUi = PiPiCo1GatedPlots1D.Ui_PiPiCo1GatedPlots1D()
        self.PiPiCoGPlots1DUi.setupUi(self)
        
  
        self.Plots1DPlotWidget= pg.PlotWidget()
        self.PiPiCoGPlots1DUi.horizontalLayout.insertWidget(0, self.Plots1DPlotWidget)
        self.Plots1DCurve = self.Plots1DPlotWidget.plot(pen='r')
        self.Plots1DPlotWidget.setLabel('left', 'Yield')# units='A')
        self.Plots1DPlotWidget.setLabel('bottom', 'Angle (rad)')  
        
        self.Plots1DPlotWidget1= pg.PlotWidget()
        self.PiPiCoGPlots1DUi.horizontalLayout.insertWidget(0, self.Plots1DPlotWidget1)
        self.Plots1DCurve1 = self.Plots1DPlotWidget1.plot(pen='r')
        self.Plots1DPlotWidget1.setLabel('left', 'Yield')# units='A')
        self.Plots1DPlotWidget1.setLabel('bottom', 'Radius (pixel)')                 
        
        self.show()

class PiPiCoGPlots1(QtGui.QMainWindow):
    def __init__(self, parent=None):

        super(PiPiCoGPlots1, self).__init__()
        
        self.pos, self.colors = zip(*cmapToColormap(matplotlib.cm.jet))
        # Set the colormap
        self.clrmp =  pg.ColorMap(self.pos, self.colors)
        
        self.PiPiCoGPlotsUi = PiPiCo1GatedPlots.Ui_PiPiCo1GatedPlots()
        self.PiPiCoGPlotsUi.setupUi(self)
        
        self.PiPiCoItem = pg.PlotItem(title = 'PiPiCo1',labels={'bottom': ('T', 'ns'), 'left': ('T', 'ns')})
        self.PiPiCoItem.setAspectLocked(False)                      
        self.PiPiCoPlot = pg.ImageView(name='PiPiCo1', view=self.PiPiCoItem) 
        self.PiPiCoPlot.setColorMap(self.clrmp)   
        self.PiPiCoPlot.view.invertY(False)              
        self.PiPiCoGPlotsUi.Tof.insertWidget(0, self.PiPiCoPlot)   

        
        self.XYItem = pg.PlotItem(title = 'XY',labels={'bottom': ('X', 'mm'), 'left': ('Y', 'mm')})
        self.XYItem.setAspectLocked(False)
        self.XYPlot = pg.ImageView(name='XY', view=self.XYItem) 
        self.XYPlot.setColorMap(self.clrmp) 
        self.XYPlot.view.invertY(False)
        self.PiPiCoGPlotsUi.XY.insertWidget(0, self.XYPlot)
        
        self.XTItem = pg.PlotItem(title = 'XT',labels={'bottom': ('T', 'ns'), 'left': ('X', 'mm')})
        self.XTItem.setAspectLocked(False)
        self.XTPlot = pg.ImageView(name='XT', view=self.XTItem) 
        self.XTPlot.setColorMap(self.clrmp) 
        self.XTPlot.view.invertY(False)        
        self.PiPiCoGPlotsUi.XT.insertWidget(0, self.XTPlot)
        
        self.YTItem = pg.PlotItem(title = 'YT',labels={'bottom': ('T', 'ns'), 'left': ('Y', 'mm')})
        self.YTItem.setAspectLocked(False)
        self.YTPlot = pg.ImageView(name='YT', view=self.YTItem) 
        self.YTPlot.setColorMap(self.clrmp)    
        self.YTPlot.view.invertY(False)     
        self.PiPiCoGPlotsUi.YT.insertWidget(0, self.YTPlot)       
        
        
        self.eARItem = pg.PlotItem(title = 'eAR',labels={'bottom': ('Angle', 'rad'), 'left': ('Radius', 'pixel')})
        self.eARItem.setAspectLocked(False)                      
        self.eARPlot = pg.ImageView(name='eAR', view=self.eARItem) 
        self.eARPlot.setColorMap(self.clrmp)    
        self.eARPlot.view.invertY(False)             
        self.PiPiCoGPlotsUi.PiPiCo.insertWidget(0, self.eARPlot) 
        self.eARItem.setAspectLocked(False)
        
        self.eXYItem = pg.PlotItem(title = 'eXY',labels={'bottom': ('X', 'mm'), 'left': ('Y', 'mm')})
        self.eXYItem.setAspectLocked(False)
        self.eXYPlot = pg.ImageView(name='eXY', view=self.eXYItem) 
        self.eXYPlot.setColorMap(self.clrmp)      
        self.eXYPlot.view.invertY(False)   
        self.PiPiCoGPlotsUi.eXY.insertWidget(0, self.eXYPlot)
        
        self.show()  
        

