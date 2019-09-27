
import sys
import numpy as np
import signal
import datetime
import copy
import pyqtgraph as pg
import matplotlib
from pyqtgraph.Qt import QtGui, QtCore

import Tof3GatedPlots, Tof3GatedPlots1D
#from GUIs import XYGPlots1, XYGTof3

class GateTof3():
    def __init__(self,parent):
         
        
        self.parent = parent
    
                                     
        self.tof_inds = []
        
        self.roi =  pg.LinearRegionItem([0,0])
   #     self.roiState = 0
        
     #   self.roi.sigRegionChanged.connect(lambda: self.sum_under_1d_roi())
        self.roi.sigRegionChanged.connect(lambda: self.disableMouse())
        self.roi.sigRegionChangeFinished.connect(lambda: self.enableMouse())
        self.roi.sigRegionChangeFinished.connect(lambda: self.gate_move_finished())

        
        self.roiName = 'RectGate3'

        
        self.initialize_variables()
        
        self.initialize_plots()
        


        
    def sum_under_1d_roi(self):
       # print 'sum_linear i:',i
        if self.parent.RectGate3_roiState== 0:
            return 0
        
        roi_yield = np.sum(self.parent.Tof[self.Tofind1:self.Tofind2])

        #return self.TaxisM[Tofind1], self.TaxisM[Tofind2], np.sum(self.Tof[Tofind1:Tofind2])
        self.parent.TofUi.Rect3Yield.setText(self.roiName+"Yield:%0.1f" % roi_yield)
      #  print roi_yield
        
        return roi_yield
    
        
   
        
    def disableMouse(self):
        self.parent.TofPlotWidget.setMouseEnabled(x=False, y=False)
     #   print 'disable', prts, prts.getAxis('bottom').range
     

        
    def enableMouse(self):
        self.parent.TofPlotWidget.setMouseEnabled(x=True, y=True)
        
         
    def update_ion(self, Tofind, Xind, Yind):
     
     #change here Xind to X(Xind)
        if self.parent.prt.Taxis[Tofind] > self.x_cond_s and self.parent.prt.Taxis[Tofind] < self.x_cond_l:             
      #      self.tof_inds.append(Tofind-1)           
            self.XY[Xind-1, Yind-1] += 1
            self.P += 1
            
            
    def coin(self):
     
     #change here Xind to X(Xind)
        return self.P > 0
        
    def reset_coin_var(self):
        self.P = 0
                    
             
    def update_electron(self, eAind, eRind, eXind, eYind):
     
     #change here Xind to X(Xind)

       self.eXY[eXind-1, eYind-1] += 1
       self.eAR[eAind-1, eRind-1] += 1
       self.eA[eAind,0] += 1
       self.eR[eRind,0] += 1
       #     self.XT[Tofind-1, Xind-1] += 1
       #     self.YT[Tofind-1, Yind-1] += 1   
            

           
    def gate_move_finished(self):
        print 'gate moved'
        self.initialize_variables()      
        
        

        self.x_cond_s, self.x_cond_l = self.roi.getRegion()
        print self.x_cond_s, self.x_cond_l
        
#        self.XYG_ind1 = np.array([(self.Xaxis>self.x_cond_s) & (self.Xaxis<self.x_cond_l)], dtype= np.bool)
        self.Tofind1 = next((Tof_ind for Tof_ind, Tof_ele in enumerate(self.parent.prt.Taxis) if Tof_ele > self.x_cond_s),None) 
        self.Tofind2 = next((Tof_ind for Tof_ind, Tof_ele in enumerate(self.parent.prt.Taxis) if Tof_ele > self.x_cond_l),None) 
     #   print  self.Tofind1, self.Tofind2, self.Taxis[self.Tofind1], self.Taxis[self.Tofind2]


        self.sum_under_1d_roi()
        
    def initialize_variables(self):
    
    
        self.shot_num = 0            
        self.P = 0     
       

        self.old_count = 0
        self.new_count = 0    
                     
        self.XY = np.zeros([self.parent.prt.Xbinnum-1, self.parent.prt.Ybinnum-1])
        self.eXY = np.zeros([self.parent.prt.eXbinnum-1, self.parent.prt.eYbinnum-1])
        self.eAR = np.zeros([self.parent.prt.eAbinnum-1, self.parent.prt.eRbinnum-1])
        self.eA = np.zeros([self.parent.prt.eAbinnum-1, 1])
        self.eR = np.zeros([self.parent.prt.eRbinnum-1, 1])                        
    #    self.Tof = np.zeros([self.Tbinnum-1,1])
     #   self.XT = np.zeros([self.Tbinnum-1, self.Xbinnum-1])
     #   self.YT = np.zeros([self.Tbinnum-1, self.Ybinnum-1])
#        self.TSumX = np.zeros([self.Tbinnum-1,1])
 #       self.TSumY = np.zeros([self.Tbinnum-1,1])
#        self.X_arr  = np.arange(len(self.Xbinnum-1))
 #       self.Y_arr  = np.arange(len(self.Ybinnum-1))
    #    self.PiPiCo = np.zeros([self.Tbinnum-2,self.Tbinnum-2])  
        
       # self.XYG_ind1 = np.array([],dtype=np.bool)
       # self.XYG_ind2 = np.array([],dtype=np.bool)
        
       # print 'XYG shape1:', self.XYG.shape
#        print self.XYG_ind1, self.XYG_ind2 
        
        
    def initialize_plots(self):
         
        self.plotWindow = TofGPlots3()   
        self.plot1dWindow = TofGPlots1D3()           
        
    def update_plots(self):
    
       # QtGui.QApplication.processEvents()
        self.sum_under_1d_roi()        
     #   self.tofWindow.TofCurve.setData(np.squeeze(self.TaxisM[self.Tofind1:self.Tofind2]),np.squeeze(self.parent.Tof[self.Tofind1:self.Tofind2]))
        self.plot1dWindow.Plots1DCurve.setData(np.squeeze(self.parent.prt.eAaxisM),np.squeeze(self.eA))
        self.plot1dWindow.Plots1DCurve1.setData(np.squeeze(self.parent.prt.eRaxisM),np.squeeze(self.eR))     
        
     #   print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
      #  print self.x_cond_s, self.x_cond_l, self.y_cond_s, self.y_cond_l, self.XYG.shape, self.XYG_ind1.shape,self.XYG_ind2.shape, self.parent.XY.shape
       # print self.parent.XY.shape
        #self.XYG = self.parent.XY[self.XYG_ind1, self.XYG_ind2]
      
        self.max_XY = self.XY.max()
        self.XY_norm = self.XY
     #   pos_XY = np.array([0.0, max_XY/2, max_XY])
     #   color_XY = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XY = pg.ColorMap(pos_XY, color_XY)  
     #   self.XYPlot.setColorMap(clrmp_XY)           
        if self.max_XY == 0:  
           # print 'xy: true'
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
        #    print 'xy: true'
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



class TofGPlots1D3(QtGui.QMainWindow):
    def __init__(self, parent=None):

        super(TofGPlots1D3, self).__init__()
        
        
        self.TofGPlots1DUi = Tof3GatedPlots1D.Ui_Tof3GatedPlots1D()
        self.TofGPlots1DUi.setupUi(self)
        
  
        self.Plots1DPlotWidget= pg.PlotWidget()
        self.TofGPlots1DUi.horizontalLayout.insertWidget(0, self.Plots1DPlotWidget)
        self.Plots1DCurve = self.Plots1DPlotWidget.plot(pen='b')
        self.Plots1DPlotWidget.setLabel('left', 'Yield')# units='A')
        self.Plots1DPlotWidget.setLabel('bottom', 'Angle (rad)')  
        
        self.Plots1DPlotWidget1= pg.PlotWidget()
        self.TofGPlots1DUi.horizontalLayout.insertWidget(0, self.Plots1DPlotWidget1)
        self.Plots1DCurve1 = self.Plots1DPlotWidget1.plot(pen='b')
        self.Plots1DPlotWidget1.setLabel('left', 'Yield')# units='A')
        self.Plots1DPlotWidget1.setLabel('bottom', 'Radius (pixel)')     
        
        self.show()

from cmapToColormap import cmapToColormap                        
            
class TofGPlots3(QtGui.QMainWindow):
    def __init__(self, parent=None):

        super(TofGPlots3, self).__init__()
        
        self.pos, self.colors = zip(*cmapToColormap(matplotlib.cm.jet))
        # Set the colormap
        self.clrmp =  pg.ColorMap(self.pos, self.colors)
        
        self.TofGPlotsUi = Tof3GatedPlots.Ui_Tof3GatedPlots()
        self.TofGPlotsUi.setupUi(self)
        
 

        
        self.XYItem = pg.PlotItem(title = 'XY',labels={'bottom': ('X', 'mm'), 'left': ('Y', 'mm')})
        self.XYItem.setAspectLocked(False)
        self.XYPlot = pg.ImageView(name='XY', view=self.XYItem) 
        self.XYPlot.setColorMap(self.clrmp) 
        self.XYPlot.view.invertY(False)
        self.TofGPlotsUi.XY.insertWidget(0, self.XYPlot)
        
  
        
        
        self.eARItem = pg.PlotItem(title = 'eAR',labels={'bottom': ('Angle', 'rad'), 'left': ('Radius', 'pixel')})
        self.eARItem.setAspectLocked(False)                      
        self.eARPlot = pg.ImageView(name='eAR', view=self.eARItem) 
        self.eARPlot.setColorMap(self.clrmp)  
        self.eARPlot.view.invertY(False)               
        self.TofGPlotsUi.PiPiCo.insertWidget(0, self.eARPlot) 
        self.eARItem.setAspectLocked(False)
        
        self.eXYItem = pg.PlotItem(title = 'eXY',labels={'bottom': ('X', 'mm'), 'left': ('Y', 'mm')})
        self.eXYItem.setAspectLocked(False)
        self.eXYPlot = pg.ImageView(name='eXY', view=self.eXYItem) 
        self.eXYPlot.setColorMap(self.clrmp)         
        self.eXYPlot.view.invertY(False)
        self.TofGPlotsUi.eXY.insertWidget(0, self.eXYPlot)
        
        self.show()  
        

