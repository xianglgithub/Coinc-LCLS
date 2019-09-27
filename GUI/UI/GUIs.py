#GUI file for coincidence experiment online analysis
#Xiang Li 01/16/2018

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import final_Tof, final_XY, final_XT, final_YT, final_PiPiCo_push, control, final_XY_push, final_Tof_push, final_eXY_push, final_eAR_push, final_eA_push, final_eR_push

import PiPiCo1GatedPlots, PiPiCo2GatedPlots, PiPiCo3GatedPlots, PiPiCo1GatedPlots1D, PiPiCo2GatedPlots1D, PiPiCo3GatedPlots1D, Tof1GatedPlots, Tof2GatedPlots, Tof3GatedPlots, Tof1GatedTof, Tof2GatedTof, Tof3GatedTof

from GUI.GateXY1 import GateXY1

from GUI.GateTof1 import GateTof1
from GUI.GateTof2 import GateTof2
from GUI.GateTof3 import GateTof3

from GUI.GatePiPiCo1 import GatePiPiCo1
from GUI.GatePiPiCo2 import GatePiPiCo2
from GUI.GatePiPiCo3 import GatePiPiCo3

import signal, sys
import numpy as np

import matplotlib
from cmapToColormap import cmapToColormap




  

        


class eRGUI(QtGui.QMainWindow):
    def __init__(self, prt, parent=None):

        super(eRGUI, self).__init__()
                
        self.prt = prt     
        
        self.eR = np.zeros([self.prt.eRbinnum-1,1]) 
        
        self.eRUi = final_eR_push.Ui_eR()
        self.eRUi.setupUi(self)
  
        self.eRPlotWidget= pg.PlotWidget()
        self.eRUi.verticalLayout.insertWidget(0, self.eRPlotWidget)
        self.eRCurve = self.eRPlotWidget.plot(pen='w')
        self.eRPlotWidget.setLabel('left', 'Yield')# units='A')
        self.eRPlotWidget.setLabel('bottom', 'Radius (pixel)') 

class eAGUI(QtGui.QMainWindow):
    def __init__(self, prt, parent=None):

        super(eAGUI, self).__init__()
        
        self.prt = prt
        
        self.eA = np.zeros([self.prt.eAbinnum-1,1]) 
        
        self.eAUi = final_eA_push.Ui_eA()
        self.eAUi.setupUi(self)
  
        self.eAPlotWidget= pg.PlotWidget()
        self.eAUi.verticalLayout.insertWidget(0, self.eAPlotWidget)
        self.eACurve = self.eAPlotWidget.plot(pen='w')
        self.eAPlotWidget.setLabel('left', 'Yield')# units='A')
        self.eAPlotWidget.setLabel('bottom', 'Angle (rad)') 
        
      #  self.eAUi.ARG1.clicked.connect(self.addRG1)
      #  self.XYUi.ARG2.clicked.connect(self.addRG2)
      #  self.XYUi.ACG.clicked.connect(self.addCG)
        
       # self.eAUi.RRG1.clicked.connect(self.rmRG1)
        #self.RectGate1_roiState = 0


class TofGUI(QtGui.QMainWindow):
    def __init__(self, prt, parent=None):

        super(TofGUI, self).__init__()
        
        self.prt = prt    
        
        self.Tof = np.zeros([self.prt.Tbinnum-1,1]) 
        
        self.TofUi = final_Tof_push.Ui_Tof()
        self.TofUi.setupUi(self)
  
        self.TofPlotWidget= pg.PlotWidget()
        self.TofUi.verticalLayout.insertWidget(0, self.TofPlotWidget)
        self.TofCurve = self.TofPlotWidget.plot(pen='w')
        self.TofPlotWidget.setLabel('left', 'Yield')# units='A')
        self.TofPlotWidget.setLabel('bottom', 'Tof (ns)') 
        
        self.TofUi.ARG1.clicked.connect(self.addRG1)       
        self.TofUi.RRG1.clicked.connect(self.rmRG1)
        self.RectGate1_roiState = 0
        
        self.TofUi.ARG2.clicked.connect(self.addRG2)       
        self.TofUi.RRG2.clicked.connect(self.rmRG2)
        self.RectGate2_roiState = 0
        
        self.TofUi.ARG3.clicked.connect(self.addRG3)       
        self.TofUi.RRG3.clicked.connect(self.rmRG3)
        self.RectGate3_roiState = 0                
      #  self.XYUi.RRG2.clicked.connect(self.rmRG2)
       # self.XYUi.RCG.clicked.connect(self.rmCG)  
        
#        self.RectGate1 = GateTof1(self, self.Xbin, self.Ybin, self.Tbin, self.Xmin, self.Ymin, self.Tmin, self.Xmax, self.Ymax, self.Tmax, self.Xbinnum, self.Ybinnum, self.Tbinnum)
       # self.RectGate2 = GateXY2()
       # self.RectGate3 = GateXY3()           
       
    def addRG1(self):

        self.RectGate1 = GateTof1(self)    
        
        xmin, xmax = self.TofPlotWidget.getAxis('bottom').range
        ymin, ymax = self.TofPlotWidget.getAxis('left').range              
        
        self.RectGate1.roi.setRegion([xmin/10, xmax/10])
                   # self.rois[i].setZValue(-20)
        self.RectGate1.roi.setBrush(color = QtGui.QColor(255,0,0,127))
        self.TofPlotWidget.addItem(self.RectGate1.roi)
               
        self.RectGate1_roiState = 1                      
        self.RectGate1.shot_num = 0         
        self.RectGate1.gate_move_finished()    
        self.RectGate1.sum_under_1d_roi()       
                     
        
        
        
    def rmRG1(self):
        
        self.TofPlotWidget.removeItem(self.RectGate1.roi)
        self.RectGate1_roiState = 0           
        del self.RectGate1
        
    def addRG2(self):

        self.RectGate2 = GateTof2(self)    
        
        xmin, xmax = self.TofPlotWidget.getAxis('bottom').range
        ymin, ymax = self.TofPlotWidget.getAxis('left').range              
        
        self.RectGate2.roi.setRegion([xmin/10, xmax/10])
                   # self.rois[i].setZValue(-20)
        self.RectGate2.roi.setBrush(color = QtGui.QColor(0,255,0,127))
        self.TofPlotWidget.addItem(self.RectGate2.roi)
               
        self.RectGate2_roiState = 1                      
        self.RectGate2.shot_num = 0         
        self.RectGate2.gate_move_finished()    
        self.RectGate2.sum_under_1d_roi()       
                     
        
        
        
    def rmRG2(self):
        
        self.TofPlotWidget.removeItem(self.RectGate2.roi)
        self.RectGate2_roiState = 0           
        del self.RectGate2       
        
    def addRG3(self):

        self.RectGate3 = GateTof3(self)    
        
        xmin, xmax = self.TofPlotWidget.getAxis('bottom').range
        ymin, ymax = self.TofPlotWidget.getAxis('left').range              
        
        self.RectGate3.roi.setRegion([xmin/10, xmax/10])
                   # self.rois[i].setZValue(-20)
        self.RectGate3.roi.setBrush(color = QtGui.QColor(0,0,255,127))
        self.TofPlotWidget.addItem(self.RectGate3.roi)
               
        self.RectGate3_roiState = 1                      
        self.RectGate3.shot_num = 0         
        self.RectGate3.gate_move_finished()    
        self.RectGate3.sum_under_1d_roi()       
                     
        
        
        
    def rmRG3(self):
        
        self.TofPlotWidget.removeItem(self.RectGate3.roi)
        self.RectGate3_roiState = 0           
        del self.RectGate3         
    


class XYGUI(QtGui.QMainWindow):
    def __init__(self, prt, parent=None):

        super(XYGUI, self).__init__()   
        
        self.prt = prt

        
        self.XY = np.zeros([self.prt.Xbinnum-1, self.prt.Ybinnum-1])        
        
          
        self.XYUi = final_XY_push.Ui_XY()
        self.XYUi.setupUi(self)
        
        self.XYItem = pg.PlotItem(title = 'XY',labels={'bottom': ('X', 'mm'), 'left': ('Y', 'mm')})
        self.XYItem.setAspectLocked(False)
        
                      
        self.XYPlot = pg.ImageView(name='XY', view=self.XYItem) 
        
        self.XYUi.verticalLayout.insertWidget(0, self.XYPlot)
        
        self.XYUi.ARG1.clicked.connect(self.addRG1)
      #  self.XYUi.ARG2.clicked.connect(self.addRG2)
      #  self.XYUi.ACG.clicked.connect(self.addCG)
        
        self.XYUi.RRG1.clicked.connect(self.rmRG1)
      #  self.XYUi.RRG2.clicked.connect(self.rmRG2)
       # self.XYUi.RCG.clicked.connect(self.rmCG)  
        
    #    self.RectGate1 = GateXY1(self)
       # self.RectGate2 = GateXY2()
       # self.RectGate3 = GateXY3()   
                  
        self.pos, self.colors = zip(*cmapToColormap(matplotlib.cm.jet))
        # Set the colormap
        self.clrmp =  pg.ColorMap(self.pos, self.colors)
        
     #   self.RectGate1_roiState = 0
        
        
    def addRG1(self):
        xmin, xmax = self.XYItem.getAxis('bottom').range
        ymin, ymax = self.XYItem.getAxis('left').range        
        self.RectGate1.roi.setPos([(xmin+xmax)/2, (ymin+ymax)/2])
        self.RectGate1.roi.setSize([(xmax-xmin)/10, (ymax-ymin)/10])
        self.RectGate1.roi.setPen(width=2.5,color='r')
        self.XYItem.vb.addItem(self.RectGate1.roi)
        
        self.RectGate1_roiState = 1                      
        self.RectGate1.num_shot = 0         
                 #   print 'i5:',i       
        self.RectGate1.sum_under_2d_roi()       
                     
        self.RectGate1.gate_move_finished()    
        
        
    def rmRG1(self):
        self.XYItem.vb.removeItem(self.RectGate1.roi)
        self.RectGate1_roiState = 0    
        
        
        
class eARGUI(QtGui.QMainWindow):
    def __init__(self, prt,parent=None):

        super(eARGUI, self).__init__()   
        
        
        self.prt = prt        

        
        self.eAR = np.zeros([self.prt.eAbinnum-1, self.prt.eRbinnum-1])        
        
          
        self.eARUi = final_eAR_push.Ui_eAR()
        self.eARUi.setupUi(self)
        
        self.eARItem = pg.PlotItem(title = 'eAR',labels={'bottom': ('Angle', 'rad'), 'left': ('Radius', 'pixel')})
        self.eARItem.setAspectLocked(False)
        
                      
        self.eARPlot = pg.ImageView(name='eAR', view=self.eARItem) 
        
        self.eARUi.verticalLayout.insertWidget(0, self.eARPlot)
        
    #    self.eARUi.ARG1.clicked.connect(self.addRG1)
      #  self.XYUi.ARG2.clicked.connect(self.addRG2)
      #  self.XYUi.ACG.clicked.connect(self.addCG)
        
     #   self.eARUi.RRG1.clicked.connect(self.rmRG1)
      #  self.XYUi.RRG2.clicked.connect(self.rmRG2)
       # self.XYUi.RCG.clicked.connect(self.rmCG)  
        
       # self.RectGate1 = eGateXY1(self, self.eXbin, self.Xbin, self.Ybin, self.Tbin, self.eXmin, self.Xmin, self.Ymin, self.Tmin, self.eXmax, self.Xmax, self.Ymax, self.Tmax, self.eXbinnum, self.Xbinnum, self.Ybinnum, self.Tbinnum)
       # self.RectGate2 = GateXY2()
       # self.RectGate3 = GateXY3()   
                  
        self.pos, self.colors = zip(*cmapToColormap(matplotlib.cm.jet))
        # Set the colormap
        self.clrmp =  pg.ColorMap(self.pos, self.colors)
                
        
class eXYGUI(QtGui.QMainWindow):
    def __init__(self, prt,parent=None):

        super(eXYGUI, self).__init__()   
        
        
        self.prt = prt        

        
        self.eXY = np.zeros([self.prt.eXbinnum-1, self.prt.eYbinnum-1])        
        
          
        self.eXYUi = final_eXY_push.Ui_eXY()
        self.eXYUi.setupUi(self)
        
        self.eXYItem = pg.PlotItem(title = 'eXY',labels={'bottom': ('X', 'mm'), 'left': ('Y', 'mm')})
        self.eXYItem.setAspectLocked(False)
        
                      
        self.eXYPlot = pg.ImageView(name='eXY', view=self.eXYItem) 
        
        self.eXYUi.verticalLayout.insertWidget(0, self.eXYPlot)
        
        self.eXYUi.ARG1.clicked.connect(self.addRG1)
      #  self.XYUi.ARG2.clicked.connect(self.addRG2)
      #  self.XYUi.ACG.clicked.connect(self.addCG)
        
        self.eXYUi.RRG1.clicked.connect(self.rmRG1)
      #  self.XYUi.RRG2.clicked.connect(self.rmRG2)
       # self.XYUi.RCG.clicked.connect(self.rmCG)  
        
       # self.RectGate1 = eGateXY1(self, self.eXbin, self.Xbin, self.Ybin, self.Tbin, self.eXmin, self.Xmin, self.Ymin, self.Tmin, self.eXmax, self.Xmax, self.Ymax, self.Tmax, self.eXbinnum, self.Xbinnum, self.Ybinnum, self.Tbinnum)
       # self.RectGate2 = GateXY2()
       # self.RectGate3 = GateXY3()   
                  
        self.pos, self.colors = zip(*cmapToColormap(matplotlib.cm.jet))
        # Set the colormap
        self.clrmp =  pg.ColorMap(self.pos, self.colors)
        
      #  self.RectGate1_roiState = 0
        
        
    def addRG1(self):
        xmin, xmax = self.eXYItem.getAxis('bottom').range
        ymin, ymax = self.eXYItem.getAxis('left').range        
        self.RectGate1.roi.setPos([(xmin+xmax)/2, (ymin+ymax)/2])
        self.RectGate1.roi.setSize([(xmax-xmin)/10, (ymax-ymin)/10])
        self.RectGate1.roi.setPen(width=2.5,color='r')
        self.eXYItem.vb.addItem(self.RectGate1.roi)
        
        self.RectGate1_roiState = 1                      
        self.RectGate1.num_shots = 0         
                 #   print 'i5:',i       
        self.RectGate1.sum_under_2d_roi()       
                     
        self.RectGate1.gate_move_finished()    
        
        
    def rmRG1(self):
        self.eXYItem.vb.removeItem(self.RectGate1.roi)
        self.RectGate1_roiState = 0     
            

        
class XTGUI(QtGui.QMainWindow):
    def __init__(self, parent=None):

        super(XTGUI, self).__init__()      
          
        self.XTUi = final_XT.Ui_XT()
        self.XTUi.setupUi(self)
        
        self.XTItem = pg.PlotItem(title = 'XT',labels={'bottom': ('T', 'ns'), 'left': ('X', 'mm')})
        self.XTItem.setAspectLocked(False)
        
                      
        self.XTPlot = pg.ImageView(name='XT', view=self.XTItem) 
        
        self.XTUi.verticalLayout.insertWidget(0, self.XTPlot)
        
class YTGUI(QtGui.QMainWindow):
    def __init__(self, parent=None):

        super(YTGUI, self).__init__()      
          
        self.YTUi = final_YT.Ui_YT()
        self.YTUi.setupUi(self)
        
        self.YTItem = pg.PlotItem(title = 'YT',labels={'bottom': ('T', 'ns'), 'left': ('Y', 'mm')})
        self.YTItem.setAspectLocked(False)
        
                      
        self.YTPlot = pg.ImageView(name='YT', view=self.YTItem) 
        
        self.YTUi.verticalLayout.insertWidget(0, self.YTPlot)   
        
class PiPiCoGUI(QtGui.QMainWindow):
    def __init__(self, prt, parent=None):

        super(PiPiCoGUI, self).__init__()      
        
        self.prt = prt
                                           
        self.PiPiCo = np.zeros([self.prt.Tbinnum-1, self.prt.Tbinnum-1])        
        
          
        self.PiPiCoUi = final_PiPiCo_push.Ui_PiPiCo()
        self.PiPiCoUi.setupUi(self)
        
        self.PiPiCoItem = pg.PlotItem(title = 'PiPiCo',labels={'bottom': ('T', 'ns'), 'left': ('T', 'ns')})
        self.PiPiCoItem.setAspectLocked(False)
        
                      
        self.PiPiCoPlot = pg.ImageView(name='PiPiCo', view=self.PiPiCoItem) 
        
        self.PiPiCoUi.verticalLayout.insertWidget(0, self.PiPiCoPlot)
        
        self.PiPiCoUi.ARG1.clicked.connect(self.addRG1)       
        self.PiPiCoUi.RRG1.clicked.connect(self.rmRG1)
        self.RectGate1_roiState = 0
        
        self.PiPiCoUi.ARG2.clicked.connect(self.addRG2)       
        self.PiPiCoUi.RRG2.clicked.connect(self.rmRG2)
        self.RectGate2_roiState = 0
        
        self.PiPiCoUi.ARG3.clicked.connect(self.addRG3)       
        self.PiPiCoUi.RRG3.clicked.connect(self.rmRG3)
        self.RectGate3_roiState = 0                
                  
        self.pos, self.colors = zip(*cmapToColormap(matplotlib.cm.jet))
        # Set the colormap
        self.clrmp =  pg.ColorMap(self.pos, self.colors)
        

        
        
    def addRG1(self):
    
    
        self.RectGate1 = GatePiPiCo1(self)
    
        xmin, xmax = self.PiPiCoItem.getAxis('bottom').range
        ymin, ymax = self.PiPiCoItem.getAxis('left').range        
        self.RectGate1.roi.setPos([(xmin+xmax)/2, (ymin+ymax)/2])
        self.RectGate1.roi.setSize([(xmax-xmin)/10, (ymax-ymin)/10])
        self.RectGate1.roi.setPen(width=2.5,color='r')
        self.PiPiCoItem.vb.addItem(self.RectGate1.roi)
        
        self.RectGate1_roiState = 1                      
        self.RectGate1.shot_num = 0         
                 #   print 'i5:',i       
        self.RectGate1.sum_under_2d_roi()       
                     
        self.RectGate1.gate_move_finished()    
        
        
    def rmRG1(self):
        self.PiPiCoItem.vb.removeItem(self.RectGate1.roi)
        self.RectGate1_roiState = 0    
        
    def addRG2(self):
    
    
        self.RectGate2 = GatePiPiCo2(self)
    
        xmin, xmax = self.PiPiCoItem.getAxis('bottom').range
        ymin, ymax = self.PiPiCoItem.getAxis('left').range        
        self.RectGate2.roi.setPos([(xmin+xmax)/2, (ymin+ymax)/2])
        self.RectGate2.roi.setSize([(xmax-xmin)/10, (ymax-ymin)/10])
        self.RectGate2.roi.setPen(width=2.5,color='g')
        self.PiPiCoItem.vb.addItem(self.RectGate2.roi)
        
        self.RectGate2_roiState = 1                      
        self.RectGate2.shot_num = 0         
                 #   print 'i5:',i       
        self.RectGate2.sum_under_2d_roi()       
                     
        self.RectGate2.gate_move_finished()    
        
        
    def rmRG2(self):
        self.PiPiCoItem.vb.removeItem(self.RectGate2.roi)
        self.RectGate2_roiState = 0         

    def addRG3(self):
    
    
        self.RectGate3 = GatePiPiCo3(self)
    
        xmin, xmax = self.PiPiCoItem.getAxis('bottom').range
        ymin, ymax = self.PiPiCoItem.getAxis('left').range        
        self.RectGate3.roi.setPos([(xmin+xmax)/2, (ymin+ymax)/2])
        self.RectGate3.roi.setSize([(xmax-xmin)/10, (ymax-ymin)/10])
        self.RectGate3.roi.setPen(width=2.5,color='k')
        self.PiPiCoItem.vb.addItem(self.RectGate3.roi)
        
        self.RectGate3_roiState = 1                      
        self.RectGate3.shot_num = 0         
                 #   print 'i5:',i       
        self.RectGate3.sum_under_2d_roi()       
                     
        self.RectGate3.gate_move_finished()    
        
        
    def rmRG3(self):
        self.PiPiCoItem.vb.removeItem(self.RectGate3.roi)
        self.RectGate3_roiState = 0             
                
        
class ControlPanel(QtGui.QWidget):
    def __init__(self,parent=None):
        super(ControlPanel, self).__init__()
        self.ControlP = control.Ui_ControlPanel()
        self.ControlP.setupUi(self)     
        
        
def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    
    XYG1 = XYGPlots1()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()   
   
