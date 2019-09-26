
import sys
import numpy as np
import signal
import datetime
import copy
import pyqtgraph as pg
import matplotlib



from UI.GUIs import XYGPlots3, XYGTof3

class GateXY3():
    def __init__(self,monitor_params):
         
         
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
                     

         

        self.x_cond_s = None
        self.x_cond_s = None
        self.y_cond_l = None
        self.y_cond_l = None
                
        
        self.initialize_variables()
        
        self.initialize_plots()
         
    def update_variables(self, TofInd, XInd, YInd, eXInd, eYInd):
     
        if XInd > self.x_cond_s and XInd < self.x_cond_l and YInd > self.y_cond_s and YInd < self.y_cond_l:             
            self.tof_inds.append(Tofind-1)           
            self.Tof[Tofind-1] += 1
            self.XT[Tofind-1, Xind-1] += 1
            self.YT[Tofind-1, Yind-1] += 1   
            
    def update_PiPiCo(self):
        if len(self.tof_inds) > 1:
           for i_tof_ind in range(len(self.tof_inds)-1):
             #   print '****************************************',self.PiPiCo.shape, len(self.tof_inds)
               self.PiPiCo[self.tof_inds[i_tof_ind],self.tof_inds[(i_tof_ind+1):]]  += 1
           # print self.PiPiCo.shape     
           
    def gate_moved(self):
        self.initialize_variables()       
         
    def initialize_variables(self):
                     
        self.XY = np.zeros([self.Xbinnum-1, self.Ybinnum-1])
        self.Tof = np.zeros([self.Tbinnum-1,1])
        self.XT = np.zeros([self.Tbinnum-1, self.Xbinnum-1])
        self.YT = np.zeros([self.Tbinnum-1, self.Ybinnum-1])
        self.TSumX = np.zeros([self.Tbinnum-1,1])
        self.TSumY = np.zeros([self.Tbinnum-1,1])
        
        self.PiPiCo = np.zeros([self.Tbinnum-2,self.Tbinnum-2])  
        
    def initialize_plots(self):
         
        self.plotWindow = XYGPlots3() 
        self.tofWindow = XYGTof3()          
        
    def update_images(self):
    
       # QtGui.QApplication.processEvents()
        
        self.tofWindow.TofCurve.setData(np.squeeze(self.TaxisM),np.squeeze(self.Tof))
        
        self.max_XY = self.XY.max()
        self.XY_norm = self.XY
     #   pos_XY = np.array([0.0, max_XY/2, max_XY])
     #   color_XY = np.array([[0,0,0,255], [255,128,0,255], [255,255,0,255]], dtype=np.ubyte)
     #   clrmp_XY = pg.ColorMap(pos_XY, color_XY)  
     #   self.XYPlot.setColorMap(clrmp_XY)           
        if self.max_XY != 0:  
            self.XY_norm = self.XY/self.max_XY   
            self.plotWindow.XYPlot.setImage(self.XY_norm, autoRange = False, pos = [self.Xmin, self.Ymin], scale = [self.Xbin, self.Ybin])
            
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
            self.plotWindow.PiPiCoPlot.setImage(self.PiPiCo/self.max_PiPiCo, autoRange = False, pos = [self.Tmin, self.Tmin], scale = [self.Tbin, self.Tbin])
            self.plotWindow.PiPiCoItem.setAspectLocked(False)            
            

