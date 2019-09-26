import numpy as np
from processing_layer.algorithms.CalcMomenEng import *
import time

from lib.onda.utils import (
    global_params as gp,
    dynamic_import as dyn_imp
)

de_layer = dyn_imp.import_layer_module('data_extraction_layer',
                                       gp.monitor_params)
                                       
extractE = getattr(de_layer, 'extractE')

from ImgAlgos.PyAlgos import PyAlgos

import psana
from mpi4py import MPI

class PiPiCoGate():
    def __init__(self, parent, gateName, tof1s, tof1l, tof2s, tof2l,thresh1,thresh2,ang_f):
        self.parent = parent
        self.gateName = gateName
        self.tof1s = tof1s
        self.tof1l = tof1l
        self.tof2s = tof2s
        self.tof2l = tof2l
        
        self.extractE = extractE
        

        
        self.PiPiCo_ind1 = (self.parent.TaxisM>self.tof1s) & (self.parent.TaxisM<self.tof1l)
        self.PiPiCo_ind2 = (self.parent.TaxisM>self.tof2s) & (self.parent.TaxisM<self.tof2l)    
        
        self.thresh1 = thresh1  
        self.thresh2 = thresh2 
        self.ang_f = ang_f    
        
        self.cos_theta_f1 = np.cos(0.5*self.ang_f*np.pi/180)     
        self.cos_theta_f2 = np.cos((90-0.5*self.ang_f)*np.pi/180)        
        self.cos_theta_f3 = -np.cos((90-0.5*self.ang_f)*np.pi/180)             
        self.cos_theta_f4 = -np.cos(0.5*self.ang_f*np.pi/180)                                  
                          
        self.particle1 = self.gateName[:2]
        self.particle2 = self.gateName[2:4]   
        
        self.alg = PyAlgos()        
        self.alg.set_peak_selection_pars(npix_min=self.parent.npix_min, npix_max=self.parent.npix_max, amax_thr=self.parent.amax_thr, atot_thr=self.parent.atot_thr, son_min=self.parent.son_min)     
              
                             
        
        self.init_vars()
    
    def init_vars(self):
        
        self.temp_len_run = -1
        self.temp_irun = -1

        self.num_events = 0
        
        self.num_eventss = 0

        self.num_eventsl = 0   
        
        self.num_eventsm = 0                        
        self.num_events_orth = 0
        self.num_events_para = 0      
        
        self.num_events_f = 0
        
        self.num_eventss_f = 0

        self.num_eventsl_f = 0   
        
        self.num_eventsm_f = 0                        
        self.num_events_orth_f = 0
        self.num_events_para_f = 0                     
               
    
        self.P1 = 0
        self.P2 = 0
        self.P12 = 0   
        
              

        self.Ps = 0
        self.Pl = 0     
        
        
        self.Pm = 0        
        self.P_orth = 0
        self.P_para = 0   
                        
                          
                                          
                             
  #      self.XY = np.zeros([self.parent.Xbinnum-1, self.parent.Ybinnum-1])
  #      self.XT = np.zeros([self.parent.Tbinnum-1, self.parent.Xbinnum-1])
  #      self.YT = np.zeros([self.parent.Tbinnum-1, self.parent.Ybinnum-1])       
   #     self.PiPiCo = np.zeros([self.parent.Tbinnum-2,self.parent.Tbinnum-2])       
             
         
        self.tempX1ind = []
        self.tempY1ind = []      
        
        self.tempX2ind = []
        self.tempY2ind = []    
        
        self.tempX1 = []
        self.tempY1 = []      
        self.tempT1 = []    
        self.tempT1_f = []
          
                
        self.tempX2 = []
        self.tempY2 = [] 
        self.tempT2 = []     
        self.tempT2_f = []                 
        
        self.tempXe = []
        self.tempYe = []  

        self.tempXef1 = []
        self.tempYef1 = []
        self.tempXef2 = []
        self.tempYef2 = []        
        
        self.tempEr = []

        self.tempErf1 = []

        self.tempErf2 = []
                
        
        self.tempEng1_arr = []            
        self.tempPx1_arr = []
        self.tempPy1_arr = []      
        self.tempPz1_arr = []    
                 
                
        self.tempEng2_arr = []                
        self.tempPx2_arr = []
        self.tempPy2_arr = []      
        self.tempPz2_arr = []   
        
        self.tempEng1ind_arr = []                                  
        self.tempPx1ind_arr = []
        self.tempPy1ind_arr = []      
        self.tempPz1ind_arr = [] 
        
        self.tempEng2ind_arr = []                          
        self.tempPx2ind_arr = []
        self.tempPy2ind_arr = []      
        self.tempPz2ind_arr = []    
        
        self.tempX1ind_arr = []
        self.tempY1ind_arr = []      
        
        self.tempX2ind_arr = []
        self.tempY2ind_arr = []    
        
        self.hists_pipico = {}
        
        self.hists_pipico_all = {}        
        
        for hist_name in self.parent.hist_names_pipico:
            if hist_name=='pipico':
                x_name = self.parent.monitor_params[hist_name]['x']
                x_bin = self.parent.monitor_params[x_name]['bin']       
                y_name = self.parent.monitor_params[hist_name]['y']
                y_bin = self.parent.monitor_params[y_name]['bin']    
                
                self.pipico_xbin = x_bin
                self.pipico_ybin = y_bin  
                
                x_binnum = int((self.tof1l - self.tof1s)/x_bin)+1
                y_binnum = int((self.tof2l - self.tof2s)/y_bin)+1    
                
                self.pipico_xaxis = np.linspace(self.tof1s, self.tof1l, x_binnum) 
                self.pipico_yaxis = np.linspace(self.tof2s, self.tof2l, y_binnum) 
                                            
                self.hists_pipico[hist_name] = np.zeros([x_binnum-1, y_binnum-1])      
                if self.parent.role == 'master':
                    self.hists_pipico_all[hist_name] = np.zeros([x_binnum-1, y_binnum-1]) 
                else:
                    self.hists_pipico_all[hist_name] = None       
                continue

                               
            x_name = self.parent.monitor_params[hist_name]['x']
            x_binnum = self.parent.vars_binnum[x_name]
            if 'y' in self.parent.monitor_params[hist_name].keys():
                y_name = self.parent.monitor_params[hist_name]['y']
                y_binnum = self.parent.vars_binnum[y_name]
                if 'z' in self.parent.monitor_params[hist_name].keys():
                    z_name = self.parent.monitor_params[hist_name]['z']
                    z_binnum = self.parent.vars_binnum[z_name] 
                    self.hists_pipico[hist_name] = np.zeros([x_binnum-1, y_binnum-1, z_binnum-1])
                    if self.parent.role == 'master':
                        self.hists_pipico_all[hist_name] = np.zeros([x_binnum-1, y_binnum-1, z_binnum-1])
                    else:
                        self.hists_pipico_all[hist_name] = None
                    
                else:
                    self.hists_pipico[hist_name] = np.zeros([x_binnum-1, y_binnum-1])     
                    if self.parent.role == 'master':
                        self.hists_pipico_all[hist_name] = np.zeros([x_binnum-1, y_binnum-1])
                    else:
                        self.hists_pipico_all[hist_name] = None                        
            else:
                self.hists_pipico[hist_name] = np.zeros([x_binnum-1])
                if self.parent.role == 'master':
                    self.hists_pipico_all[hist_name] = np.zeros([x_binnum-1])
                else:
                    self.hists_pipico_all[hist_name] = None                                              
        
 
        

        
    def update_ion(self, Tofind, Xind, Yind, Tofele, Xele, Yele):
     
        if (self.parent.TaxisM[Tofind] > self.tof1s and self.parent.TaxisM[Tofind] < self.tof1l):             

            self.P1 += 1
            
        #    self.tempX1ind.append(Xind)
        #    self.tempY1ind.append(Yind)  
            
            self.tempX1.append(Xele)
            self.tempY1.append(Yele)               
            self.tempT1.append(Tofele)                                             
            
        if (self.parent.TaxisM[Tofind] > self.tof2s and self.parent.TaxisM[Tofind] < self.tof2l):

            self.P2 += 1
            
       #     self.tempX2ind.append(Xind)
       #     self.tempY2ind.append(Yind)  
            
            self.tempX2.append(Xele)
            self.tempY2.append(Yele)               
            self.tempT2.append(Tofele)  
            
        if (self.parent.TaxisM[Tofind] > self.tof1s and self.parent.TaxisM[Tofind] < self.tof1l) and (self.parent.TaxisM[Tofind] > self.tof2s and self.parent.TaxisM[Tofind] < self.tof2l):

            self.P12 += 1 
            
    def is_coin(self):
    
        return (self.P1 > 0 and self.P2 > 0 and self.P12 == 0) or self.P12 > 1    
                     
      
       
    def update_electron(self, eAind, eRind, eXind, eYind, pho_ind, pls_ind):
            
        
        self.tempXe.append(eXind)
        self.tempYe.append(eYind)  
        self.tempEr.append(eRind)      
        


        
  #  def update_ion(self, Tofind, Xind, Yind):
  #  
   #     self.XY[Xind, Yind] += 1
   #     self.XT[Tind, Xind] += 1
   #     self.YT[Tind, Yind] += 1                
        
                
    def update_shotinfo(self, pho_ind, pls_ind,pho_eng,pls_eng):
   
           
        
        
        temp_num_particles_ind1 = next((tNP_ind1 for tNP_ind1, tNP_ele1 in enumerate(self.parent.vars_axis['num_particles']) if tNP_ele1 > self.P1),0)-1
        temp_num_particles_ind2 = next((tNP_ind2 for tNP_ind2, tNP_ele2 in enumerate(self.parent.vars_axis['num_particles']) if tNP_ele2 > self.P2),0)-1  
        
        if temp_num_particles_ind1 != -1:
            self.hists_pipico['num_particles1_'][temp_num_particles_ind1] += 1     
            
        
        if temp_num_particles_ind2 != -1:
            self.hists_pipico['num_particles2_'][temp_num_particles_ind2] += 1                                      
        
        for itemp1 in range(len(self.tempX1)):
              
            
            tempEng1, tempPx1, tempPy1, tempPz1 = EngMo(self.tempT1[itemp1],
            self.tempX1[itemp1],self.tempY1[itemp1],self.parent.tsim[self.particle1],
            self.parent.xcenter,self.parent.ycenter,self.parent.toff[self.particle1],self.particle1)
            
               
            tempEng_ind1 = next((tEng_ind1 for tEng_ind1, tEng_ele1 in enumerate(self.parent.vars_axis['eng']) if tEng_ele1 > tempEng1),0)-1
            tempPx_ind1 = next((tPx_ind1 for tPx_ind1, tPx_ele1 in enumerate(self.parent.vars_axis['px']) if tPx_ele1 > tempPx1),0)-1
            tempPy_ind1 = next((tPy_ind1 for tPy_ind1, tPy_ele1 in enumerate(self.parent.vars_axis['py']) if tPy_ele1 > tempPy1),0)-1                        
            tempPz_ind1 = next((tPz_ind1 for tPz_ind1, tPz_ele1 in enumerate(self.parent.vars_axis['pz']) if tPz_ele1 > tempPz1),0)-1            
            
            if tempEng_ind1 != -1 and tempPx_ind1 != -1 and tempPy_ind1 != -1 and tempPz_ind1 != -1:
            
              #  self.Eng1[tempEng_ind1-1] += 1
            #    self.Momen1[tempPx_ind1-1, tempPy_ind1-1, tempPz_ind1-1] += 1 
                            
                self.tempEng1_arr.append(tempEng1)
                self.tempPx1_arr.append(tempPx1)    
                self.tempPy1_arr.append(tempPy1)    
                self.tempPz1_arr.append(tempPz1)   
                
                self.tempEng1ind_arr.append(tempEng_ind1)
                self.tempPx1ind_arr.append(tempPx_ind1)    
                self.tempPy1ind_arr.append(tempPy_ind1)    
                self.tempPz1ind_arr.append(tempPz_ind1)  
                
                self.tempT1_f.append(self.tempT1[itemp1])
                
          #      self.tempX1ind_arr.append(self.tempX1ind[itemp1])
           #     self.tempY1ind_arr.append(self.tempY1ind[itemp1])    
                                
            
        for itemp2 in range(len(self.tempX2)):            
                        
            tempEng2, tempPx2, tempPy2, tempPz2 = EngMo(self.tempT2[itemp2],
            self.tempX2[itemp2],self.tempY2[itemp2],self.parent.tsim[self.particle2],
            self.parent.xcenter,self.parent.ycenter,self.parent.toff[self.particle2],self.particle2)            
               
            tempEng_ind2 = next((tEng_ind2 for tEng_ind2, tEng_ele2 in enumerate(self.parent.vars_axis['eng']) if tEng_ele2 > tempEng2),0)-1
            tempPx_ind2 = next((tPx_ind2 for tPx_ind2, tPx_ele2 in enumerate(self.parent.vars_axis['px']) if tPx_ele2 > tempPx2),0)-1
            tempPy_ind2 = next((tPy_ind2 for tPy_ind2, tPy_ele2 in enumerate(self.parent.vars_axis['py']) if tPy_ele2 > tempPy2),0)-1                        
            tempPz_ind2 = next((tPz_ind2 for tPz_ind2, tPz_ele2 in enumerate(self.parent.vars_axis['pz']) if tPz_ele2 > tempPz2),0)-1              
            
            if tempEng_ind2 != -1 and tempPx_ind2 != -1 and tempPy_ind2 != -1 and tempPz_ind2 != -1:
            
              #  self.Eng2[tempEng_ind2-1] += 1
             #   self.Momen2[tempPx_ind2-1, tempPy_ind2-1, tempPz_ind2-1] += 1  
                            
                self.tempEng2_arr.append(tempEng2)
                self.tempPx2_arr.append(tempPx2)    
                self.tempPy2_arr.append(tempPy2)    
                self.tempPz2_arr.append(tempPz2)  
                
                self.tempEng2ind_arr.append(tempEng_ind2)
                self.tempPx2ind_arr.append(tempPx_ind2)    
                self.tempPy2ind_arr.append(tempPy_ind2)    
                self.tempPz2ind_arr.append(tempPz_ind2)   
                
                self.tempT2_f.append(self.tempT2[itemp2])                
                
          #      self.tempX2ind_arr.append(self.tempX2ind[itemp2])
          #      self.tempY2ind_arr.append(self.tempY2ind[itemp2])  
                                                 
                
        for i1 in range(len(self.tempEng1_arr)):
            for i2 in range(len(self.tempEng2_arr)):      
                tempEng = self.tempEng1_arr[i1] + self.tempEng2_arr[i2]  
                tempPx = self.tempPx1_arr[i1] + self.tempPx2_arr[i2]       
                tempPy = self.tempPy1_arr[i1] + self.tempPy2_arr[i2]                  
                tempPz = self.tempPz1_arr[i1] + self.tempPz2_arr[i2]               
                
                if np.abs(tempPx) > self.parent.pxf or np.abs(tempPy) > self.parent.pyf or np.abs(tempPz) > self.parent.pzf or tempEng<1:
                    continue
                    
                tempT1_ind = next((t1_ind for t1_ind, t1_ele in enumerate(self.pipico_xaxis) if t1_ele > self.tempT1_f[i1]),0)-1     
                tempT2_ind = next((t2_ind for t2_ind, t2_ele in enumerate(self.pipico_yaxis) if t2_ele > self.tempT2_f[i2]),0)-1    
                
                if tempT1_ind != -1 and tempT2_ind != -1:
                    self.hists_pipico['pipico'][tempT1_ind,tempT2_ind] += 1                
                                               
                
                tempEng_ind = next((tEng_ind for tEng_ind, tEng_ele in enumerate(self.parent.vars_axis['eng']) if tEng_ele > tempEng),0)-1
                tempEng_a_ind = next((tEng_ind for tEng_ind, tEng_ele in enumerate(self.parent.vars_axis['eng_a']) if tEng_ele > tempEng),0)-1                
                tempPx_ind = next((tPx_ind for tPx_ind, tPx_ele in enumerate(self.parent.vars_axis['px']) if tPx_ele > tempPx),0)-1
                tempPy_ind = next((tPy_ind for tPy_ind, tPy_ele in enumerate(self.parent.vars_axis['py']) if tPy_ele > tempPy),0)-1                        
                tempPz_ind = next((tPz_ind for tPz_ind, tPz_ele in enumerate(self.parent.vars_axis['pz']) if tPz_ele > tempPz),0)-1  
                
               # tempPx1_ind = next((tPx1_ind for tPx1_ind, tPx1_ele in enumerate(self.parent.PXaxis) if tPx1_ele > tempPx1[i1]),0)
               # tempPy1_ind = next((tPy1_ind for tPy1_ind, tPy1_ele in enumerate(self.parent.PYaxis) if tPy1_ele > tempPy1[i1]),0)                        
               # tempPz1_ind = next((tPz1_ind for tPz1_ind, tPz1_ele in enumerate(self.parent.PZaxis) if tPz1_ele > tempPz1[i1]),0)
                                                        
                                                   
                
                if tempEng_ind != -1 and tempPx_ind != -1 and tempPy_ind != -1 and tempPz_ind != -1:    
                

                                                                                
                    self.hists_pipico['eng_'][tempEng_ind] += 1
                    
                    self.hists_pipico['eng_a_'][tempEng_a_ind] += 1
                    self.hists_pipico['eng_a_pho_'][tempEng_a_ind] += pho_eng                                                                     
                    self.hists_pipico['eng_a_pls_'][tempEng_a_ind] += pls_eng       
                    self.hists_pipico['eng_a_er'][tempEng_a_ind,self.tempEr] += 1
                   # self.Momen[tempPx_ind-1, tempPy_ind-1, tempPz_ind-1] += 1  
                    
                    self.hists_pipico['pxsum_'][tempPx_ind] += 1 
                    self.hists_pipico['pysum_'][tempPy_ind] += 1 
                    self.hists_pipico['pzsum_'][tempPz_ind] += 1 
                    
                  #  self.Momenf1[self.tempPx1ind_arr[i1], self.tempPy1ind_arr[i1], self.tempPz1ind_arr[i1]] += 1             
                  #  self.Momenf2[self.tempPx2ind_arr[i2], self.tempPy2ind_arr[i2], self.tempPz2ind_arr[i2]] += 1    
                    
                 #   self.X1Y1[self.tempX1ind_arr[i1],self.tempY1ind_arr[i1]] += 1
                 #   self.X2Y2[self.tempX2ind_arr[i2],self.tempY2ind_arr[i2]] += 1                    
                    
                    cos_theta = tempPx/np.sqrt(tempPx**2 + tempPy**2 + tempPz**2)   
                    
                    cos_theta_orth = tempPy/np.sqrt(tempPx**2 + tempPy**2 + tempPz**2)                       
                    
                    
                    if cos_theta >= self.cos_theta_f1 or cos_theta <= self.cos_theta_f4:
                        self.hists_pipico['eng_para_'][tempEng_ind] += 1
                        
                    #    self.Eng1_para[self.tempEng1ind_arr[i1]] += 1
                    #    self.Eng2_para[self.tempEng2ind_arr[i2]] += 1                        
                      #  self.Momens1[self.tempPx1ind_arr[i1], self.tempPy1ind_arr[i1], self.tempPz1ind_arr[i1]] += 1             
                      #  self.Momens2[self.tempPx2ind_arr[i2], self.tempPy2ind_arr[i2], self.tempPz2ind_arr[i2]] += 1 
                                                                                      
                        self.P_para += 1
                        
                  #  elif cos_theta >= self.cos_theta_f3 and cos_theta <= self.cos_theta_f2:
                  #      self.Eng_orth[tempEng_ind] += 1
                    elif cos_theta_orth >= self.cos_theta_f1 or cos_theta_orth <= self.cos_theta_f4:
                        self.hists_pipico['eng_orth_'][tempEng_ind] += 1                  
                        
                    #    self.Eng1_orth[self.tempEng1ind_arr[i1]] += 1
                    #   self.Eng2_orth[self.tempEng2ind_arr[i2]] += 1                        
                      #  self.Momenl1[self.tempPx1ind_arr[i1], self.tempPy1ind_arr[i1], self.tempPz1ind_arr[i1]] += 1             
                      #  self.Momenl2[self.tempPx2ind_arr[i2], self.tempPy2ind_arr[i2], self.tempPz2ind_arr[i2]] += 1 
                                                
                      #  self.Momenl[tempPx_ind, tempPy_ind, tempPz_ind] += 1                                                  
                        self.P_orth += 1 
                        
                                                          
                    
                    if tempEng < self.thresh1:
                        self.hists_pipico['eng_s_'][tempEng_ind] += 1
                        
                     #   self.Engs1[self.tempEng1ind_arr[i1]-1] += 1
                      #  self.Engs2[self.tempEng2ind_arr[i2]-1] += 1                        
                      #  self.Momens1[self.tempPx1ind_arr[i1]-1, self.tempPy1ind_arr[i1]-1, self.tempPz1ind_arr[i1]-1] += 1             
                      #  self.Momens2[self.tempPx2ind_arr[i2]-1, self.tempPy2ind_arr[i2]-1, self.tempPz2ind_arr[i2]-1] += 1 
                                                                                      
                        self.Ps += 1
                        
                    elif tempEng >= self.thresh1 and tempEng < self.thresh2:
                        self.hists_pipico['eng_m_'][tempEng_ind] += 1
                        
                      #  self.Engm1[self.tempEng1ind_arr[i1]-1] += 1
                      #  self.Engm2[self.tempEng2ind_arr[i2]-1] += 1                        
                      #  self.Momenm1[self.tempPx1ind_arr[i1]-1, self.tempPy1ind_arr[i1]-1, self.tempPz1ind_arr[i1]-1] += 1             
                      #  self.Momenm2[self.tempPx2ind_arr[i2]-1, self.tempPy2ind_arr[i2]-1, self.tempPz2ind_arr[i2]-1] += 1 
                                                
                      #  self.Momenl[tempPx_ind-1, tempPy_ind-1, tempPz_ind-1] += 1                                                  
                        self.Pm += 1 
                        
                                                
                    elif tempEng >= self.thresh2:
                        self.hists_pipico['eng_l_'][tempEng_ind] += 1
                        
                      #  self.Engl1[self.tempEng1ind_arr[i1]-1] += 1
                      #  self.Engl2[self.tempEng2ind_arr[i2]-1] += 1                        
                      #  self.Momenl1[self.tempPx1ind_arr[i1]-1, self.tempPy1ind_arr[i1]-1, self.tempPz1ind_arr[i1]-1] += 1             
                      #  self.Momenl2[self.tempPx2ind_arr[i2]-1, self.tempPy2ind_arr[i2]-1, self.tempPz2ind_arr[i2]-1] += 1 
                                                
                      #  self.Momenl[tempPx_ind-1, tempPy_ind-1, tempPz_ind-1] += 1                                                  
                        self.Pl += 1 
         

        self.tempXef1, self.tempYef1,self.tempErf1,self.pho_ind_f1,self.pls_ind_f1 = self.processDataE(self.parent.irun,self.parent.ievt-1)
        self.tempXef2, self.tempYef2,self.tempErf2,self.pho_ind_f2,self.pls_ind_f2 = self.processDataE(self.parent.irun,self.parent.ievt+1)


        if self.Ps > 0:
        
            self.fill_ele(self.tempXe,self.tempYe,self.tempEr,pho_ind,pls_ind,self.hists_pipico['ex_ey_s'],self.hists_pipico['er_er_s'],
            self.hists_pipico['pho_pls_eng_s'],self.num_eventss)
 
            self.fill_ele_f(self.tempXef1,self.tempYef1,self.tempErf1,self.pho_ind_f1,self.pls_ind_f1,
            self.hists_pipico['ex_ey_s_fls1'],self.hists_pipico['er_er_s_fls1'],self.hists_pipico['pho_pls_eng_s_fls1'],self.num_eventss_f)            
            
            
            self.fill_ele_f(self.tempXef2,self.tempYef2,self.tempErf2,self.pho_ind_f2,self.pls_ind_f2,
            self.hists_pipico['ex_ey_s_fls2'],self.hists_pipico['er_er_s_fls2'],self.hists_pipico['pho_pls_eng_s_fls2'],self.num_eventss_f)    
                     
            
        if self.Pm > 0:
        
            self.fill_ele(self.tempXe,self.tempYe,self.tempEr,pho_ind,pls_ind,self.hists_pipico['ex_ey_m'],self.hists_pipico['er_er_m'],
            self.hists_pipico['pho_pls_eng_m'],self.num_eventsm)
 
            self.fill_ele_f(self.tempXef1,self.tempYef1,self.tempErf1,self.pho_ind_f1,self.pls_ind_f1,
            self.hists_pipico['ex_ey_m_fls1'],self.hists_pipico['er_er_m_fls1'],self.hists_pipico['pho_pls_eng_m_fls1'],self.num_eventsm_f)            
            
            self.fill_ele_f(self.tempXef2,self.tempYef2,self.tempErf2,self.pho_ind_f2,self.pls_ind_f2,
            self.hists_pipico['ex_ey_m_fls2'],self.hists_pipico['er_er_m_fls2'],self.hists_pipico['pho_pls_eng_m_fls2'],self.num_eventsm_f)    
                      
            
        if self.Pl > 0:
        
            self.fill_ele(self.tempXe,self.tempYe,self.tempEr,pho_ind,pls_ind,self.hists_pipico['ex_ey_l'],self.hists_pipico['er_er_l'],
            self.hists_pipico['pho_pls_eng_l'],self.num_eventsl)
 
            self.fill_ele_f(self.tempXef1,self.tempYef1,self.tempErf1,self.pho_ind_f1,self.pls_ind_f1,
            self.hists_pipico['ex_ey_l_fls1'],self.hists_pipico['er_er_l_fls1'],self.hists_pipico['pho_pls_eng_l_fls1'],self.num_eventsl_f)            
            
            self.fill_ele_f(self.tempXef2,self.tempYef2,self.tempErf2,self.pho_ind_f2,self.pls_ind_f2,
            self.hists_pipico['ex_ey_l_fls2'],self.hists_pipico['er_er_l_fls2'],self.hists_pipico['pho_pls_eng_l_fls2'],self.num_eventsl_f)         

            
        if self.P_para > 0:
        
        
            self.fill_ele(self.tempXe,self.tempYe,self.tempEr,pho_ind,pls_ind,
            self.hists_pipico['ex_ey_para'],self.hists_pipico['er_er_para'],self.hists_pipico['pho_pls_eng_para'],self.num_events_para)
 
            self.fill_ele_f(self.tempXef1,self.tempYef1,self.tempErf1,self.pho_ind_f1,self.pls_ind_f1,
            self.hists_pipico['ex_ey_para_fls1'],self.hists_pipico['er_er_para_fls1'],self.hists_pipico['pho_pls_eng_para_fls1'],self.num_events_para_f)            
            
            self.fill_ele_f(self.tempXef2,self.tempYef2,self.tempErf2,self.pho_ind_f2,self.pls_ind_f2,
            self.hists_pipico['ex_ey_para_fls2'],self.hists_pipico['er_er_para_fls2'],self.hists_pipico['pho_pls_eng_para_fls2'],self.num_events_para_f) 

        if self.P_orth > 0:
        
        
            self.fill_ele(self.tempXe,self.tempYe,self.tempEr,pho_ind,pls_ind,
            self.hists_pipico['ex_ey_orth'],self.hists_pipico['er_er_orth'],self.hists_pipico['pho_pls_eng_orth'],self.num_events_orth)            
 
            self.fill_ele_f(self.tempXef1,self.tempYef1,self.tempErf1,self.pho_ind_f1,self.pls_ind_f1,
            self.hists_pipico['ex_ey_orth_fls1'],self.hists_pipico['er_er_orth_fls1'],self.hists_pipico['pho_pls_eng_orth_fls1'],self.num_events_orth_f)            
            
            self.fill_ele_f(self.tempXef2,self.tempYef2,self.tempErf2,self.pho_ind_f2,self.pls_ind_f2,
            self.hists_pipico['ex_ey_orth_fls2'],self.hists_pipico['er_er_orth_fls2'],self.hists_pipico['pho_pls_eng_orth_fls2'],self.num_events_orth_f) 
                                          
            
        if self.Ps > 0 or self.Pl > 0 or self.Pm>0:
        
            self.fill_ele(self.tempXe,self.tempYe,self.tempEr,pho_ind,pls_ind,self.hists_pipico['ex_ey_pg'],self.hists_pipico['er_er_pg'],
            self.hists_pipico['pho_pls_eng_pg'],self.num_events)
 
            self.fill_ele_f(self.tempXef1,self.tempYef1,self.tempErf1,self.pho_ind_f1,self.pls_ind_f1,
            self.hists_pipico['ex_ey_fls1'],self.hists_pipico['er_er_pg_fls1'],self.hists_pipico['pho_pls_eng_fls1'],self.num_events_f)            
            
            self.fill_ele_f(self.tempXef2,self.tempYef2,self.tempErf2,self.pho_ind_f2,self.pls_ind_f2,
            self.hists_pipico['ex_ey_fls2'],self.hists_pipico['er_er_pg_fls2'],self.hists_pipico['pho_pls_eng_fls2'],self.num_events_f)            
                                              
      
    
    def fill_ele(self,tempXe0,tempYe0,tempEr0,pho_ind0,pls_ind0,eXY0,eReR0,pho_pls_eng0,num_events0):
            for itemp in range(len(tempXe0)):
                eXY0[tempXe0[itemp],tempYe0[itemp]] += 1   
                
            for itemp in range(len(tempEr0)):               
                eReR0[tempEr0[itemp],tempEr0] += 1  
                       
            pho_pls_eng0[pho_ind0, pls_ind0] += 1   
            num_events0 += 1    
            
    def fill_ele_f(self,tempXe0,tempYe0,tempEr0,pho_ind0,pls_ind0,eXY0,eReR0,pho_pls_eng0,num_events0):
            if len(tempXe0) > 0:
                self.fill_ele(tempXe0,tempYe0,tempEr0,pho_ind0,pls_ind0,eXY0,eReR0,pho_pls_eng0,num_events0)         
               
        
    def reset_coin_var(self):
            
        self.P1 = 0
        self.P2 = 0
        self.P12 = 0             
        
        self.tempX1ind = []
        self.tempY1ind = []      
        
        self.tempX2ind = []
        self.tempY2ind = []    
        
        self.tempX1 = []
        self.tempY1 = []      
        self.tempT1 = []  
        self.tempT1_f = []            
                
        self.tempX2 = []
        self.tempY2 = [] 
        self.tempT2 = []   
        self.tempT2_f = []                           
        
        self.tempXe = []
        self.tempYe = [] 
        
        self.tempXe_f1= []
        self.tempYe_f1= []
        self.tempXe_f2= []
        self.tempYe_f2= []     
        
        self.tempEr = []

        self.tempErf1 = []

        self.tempErf2 = []           
                    
        
        self.tempEng1_arr = []            
        self.tempPx1_arr = []
        self.tempPy1_arr = []      
        self.tempPz1_arr = []      
                
        self.tempEng2_arr = []                
        self.tempPx2_arr = []
        self.tempPy2_arr = []      
        self.tempPz2_arr = [] 
        
        self.tempEng1ind_arr = []                                          
        self.tempPx1ind_arr = []
        self.tempPy1ind_arr = []      
        self.tempPz1ind_arr = []
        
        self.tempEng2ind_arr = []                                             
        self.tempPx2ind_arr = []
        self.tempPy2ind_arr = []      
        self.tempPz2ind_arr = []    
        
        self.tempX1ind_arr = []
        self.tempY1ind_arr = []      
        
        self.tempX2ind_arr = []
        self.tempY2ind_arr = []                        
                
 #       self.num_eventss = 0
 #       self.num_eventsl = 0                

        self.Ps = 0
        self.Pl = 0   
        
        self.Pm = 0        
        self.P_orth = 0
        self.P_para = 0   
                                   
        
    def save_var(self, h5f):
        grp = h5f.create_group('PiPiCoGate_'+self.gateName)   
  #      grp.create_dataset('XY',data = self.XY)       
  #      grp.create_dataset('XT',data = self.XT)  
  #      grp.create_dataset('YT',data = self.YT)  

        grp.create_dataset('gateInfo_tof1s_tof1l_tof2s_tof2l_pipixbin_pipiybin', data=np.array([self.tof1s,self.tof1l,self.tof2s,self.tof2l,self.pipico_xbin,self.pipico_ybin]))
        
        for histname in self.parent.hist_names_pipico:   
            try:
                grp.create_dataset(histname,data = self.hists_pipico_all[histname])    
            except Exception as e:
                print(histname+' failed to be saved.')
                print(e)                                                  
        
    def reduce(self):
        for histname in self.parent.hist_names_pipico:  
            try:
                self.time_a = time.time()         
                MPI.COMM_WORLD.Reduce(self.hists_pipico[histname],self.hists_pipico_all[histname])   
                self.time_b = time.time()             
                print(histname+' reduced by '+'Rank {0} in {1:.2f} seconds'.format(self.parent.mpi_rank,self.time_b - self.time_a)) 
            except Exception as e:
                print(histname+' failed to be redueced by '+str(self.parent.mpi_rank))  
                print(e)               
        
        
    def processDataE(self,irun,ievt):
        
        if self.temp_irun != irun:
            self.psana_source = psana.DataSource(self.parent.source)
            for ii, rr in enumerate(self.psana_source.runs()):

                if ii==irun:
                    self.temp_irun = irun
                    self.temprun = rr
                    break

            self.temptimes = self.temprun.times()
            self.temp_len_run = len(self.temptimes)
            
        if ievt<0 or ievt>=self.temp_len_run:
            return [], [], [],None,None
                        
        event = {'evt': self.temprun.event(self.temptimes[ievt])}
        if event['evt'] is None:
            return [], [], [],None,None
                                                
        self.extractE(event,self)
        if self.eImage_f is None or self.pulse_eng_f is None or self.photon_eng_f is None:
            return [], [], [],None, None
            

        photon_eng_ind = next((pho_eng_ind for pho_eng_ind, pho_eng_ele in enumerate(self.parent.vars_axis['phoeng']) if pho_eng_ele > self.photon_eng_f),0)-1      
           
        pulse_eng_ind = next((pls_eng_ind for pls_eng_ind, pls_eng_ele in enumerate(self.parent.vars_axis['plseng']) if pls_eng_ele > self.pulse_eng_f),0)-1

        
        if photon_eng_ind ==-1 or pulse_eng_ind == -1:
            return [], [], [],None, None    
    
        eXinds = []
        eYinds = []
        eRinds = []
        e_peaks = self.alg.peak_finder_v4r2(self.eImage_f, thr_low=self.parent.thr_low, thr_high=self.parent.thr_high, rank=self.parent.rank, r0=self.parent.r0, dr=self.parent.dr)
        
        eXs = e_peaks[:,1].astype(int)
        eYs = e_peaks[:,2].astype(int)

        eRadius, eAngle =self.parent.cart2polar(eXs, eYs)
        
        for e_ind in range(len(eXs)):
            tempRind = next((eR_ind for eR_ind, eR_ele in enumerate(self.parent.vars_axis['er']) if eR_ele > eRadius[e_ind]),0)-1
         #   tempAind = next((eA_ind for eA_ind, eA_ele in enumerate(self.eAaxis) if eA_ele > eAngle[e_ind]),0)
            tempXind = next((eX_ind for eX_ind, eX_ele in enumerate(self.parent.vars_axis['ex']) if eX_ele > eXs[e_ind]),0)-1
            tempYind = next((eY_ind for eY_ind, eY_ele in enumerate(self.parent.vars_axis['ey']) if eY_ele > eYs[e_ind]),0)-1
           # if tempRind != 0 and tempAind != 0 and tempXind != 0 and tempYind != 0:       
            if tempXind != -1 and tempYind != -1:                  
                eXinds.append(tempXind)                 
                eYinds.append(tempYind)    
                eRinds.append(tempRind)
        if len(eXinds) > 0:
            return eXinds, eYinds, eRinds, photon_eng_ind, pulse_eng_ind
            
        else:
            return [], [],[],None,None      
    
