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

class TofGate():
    def __init__(self, parent, gateName, tofs, tofl):
        self.parent = parent
        self.gateName = gateName
        self.tofs = tofs
        self.tofl = tofl
        self.tofbin = self.parent.monitor_params['t']['bin']
        
        
        self.tof_ind = (self.parent.TaxisM>self.tofs) & (self.parent.TaxisM<self.tofl)
        

        self.particle = self.gateName
        
        self.extractE = extractE
        
        self.alg = PyAlgos()        
        self.alg.set_peak_selection_pars(npix_min=self.parent.npix_min, npix_max=self.parent.npix_max, amax_thr=self.parent.amax_thr, atot_thr=self.parent.atot_thr, son_min=self.parent.son_min)           
        
        self.init_vars()
    
    def init_vars(self):
    
    
        self.num_events = 0
             
        self.P = 0
        
        self.temp_irun = -1
        
        self.tempXef1 = []
        self.tempYef1 = []
        self.tempXef2 = []
        self.tempYef2 = []        

        self.tempErf1 = []

        self.tempErf2 = []        

        self.hists_tof = {}
        
        self.hists_tof_all = {}         
        
        
        for hist_name in self.parent.hist_names_tof:


                               
            x_name = self.parent.monitor_params[hist_name]['x']
            x_binnum = self.parent.vars_binnum[x_name]
            if 'y' in self.parent.monitor_params[hist_name].keys():
                y_name = self.parent.monitor_params[hist_name]['y']
                y_binnum = self.parent.vars_binnum[y_name]
                if 'z' in self.parent.monitor_params[hist_name].keys():
                    z_name = self.parent.monitor_params[hist_name]['z']
                    z_binnum = self.parent.vars_binnum[z_name] 
                    self.hists_tof[hist_name] = np.zeros([x_binnum-1, y_binnum-1, z_binnum-1])
                    if self.parent.role == 'master':
                        self.hists_tof_all[hist_name] = np.zeros([x_binnum-1, y_binnum-1, z_binnum-1])
                    else:
                        self.hists_tof_all[hist_name] = None
                    
                else:
                    self.hists_tof[hist_name] = np.zeros([x_binnum-1, y_binnum-1])     
                    if self.parent.role == 'master':
                        self.hists_tof_all[hist_name] = np.zeros([x_binnum-1, y_binnum-1])
                    else:
                        self.hists_tof_all[hist_name] = None                        
            else:
                self.hists_tof[hist_name] = np.zeros([x_binnum-1])
                if self.parent.role == 'master':
                    self.hists_tof_all[hist_name] = np.zeros([x_binnum-1])
                else:
                    self.hists_tof_all[hist_name] = None          

                                       
                                       
       
    def update_electron(self, eAind, eRind, eXind, eYind):
            
     #   self.eA[eAind,0] += 1            
     #   self.eR[eRind,0] += 1
        self.hists_tof['ex_ey_tg'][eXind, eYind] += 1
     #   self.eAR[eAind, eRind] += 1  
                   
         
        
    def update_ion(self, Tofind, Xind, Yind, Tofele, Xele, Yele):
        
        
        if (self.parent.TaxisM[Tofind] > self.tofs and self.parent.TaxisM[Tofind] < self.tofl):                     

            self.P += 1    
            self.hists_tof['x_y_tg'][Xind, Yind] += 1
      #      self.XT[Tofind, Xind] += 1
      #      self.YT[Tofind, Yind] += 1    

            
        
            
              
        
    def is_coin(self):
     
        return self.P > 0  
                        
        
                
    def update_shotinfo(self, pho_ind, pls_ind):
   
        self.hists_tof['pho_pls_eng_tg'][pho_ind, pls_ind] += 1   
        self.num_events += 1      
        

        
        temp_num_particles_ind = next((tNP_ind for tNP_ind, tNP_ele in enumerate(self.parent.vars_axis['num_particles']) if tNP_ele > self.P),0)-1 
               
        if temp_num_particles_ind != -1:
            self.hists_tof['num_particles_tg'][temp_num_particles_ind] += 1
            
        self.tempXef1, self.tempYef1,self.tempErf1,self.pho_ind_f1,self.pls_ind_f1 = self.processDataE(self.parent.irun,self.parent.ievt-1)
        self.tempXef2, self.tempYef2,self.tempErf2,self.pho_ind_f2,self.pls_ind_f2 = self.processDataE(self.parent.irun,self.parent.ievt+1)
        
        if len(self.tempXef1) > 0:
            for itemp in range(len(self.tempXef1)):
                self.hists_tof['ex_ey_tg_fls1'][self.tempXef1[itemp],self.tempYef1[itemp]] += 1  
                self.hists_tof['pho_pls_eng_tg_fls1'][self.pho_ind_f1, self.pls_ind_f1] += 1                   
                    
        if len(self.tempXef2) > 0:
            for itemp in range(len(self.tempXef2)):
                self.hists_tof['ex_ey_tg_fls2'][self.tempXef2[itemp],self.tempYef2[itemp]] += 1  
                self.hists_tof['pho_pls_eng_tg_fls2'][self.pho_ind_f2, self.pls_ind_f2] += 1                   
        
        
           
        
    def reset_coin_var(self):
            

              
        self.P = 0

  
                
    def save_var(self, h5f):
        grp = h5f.create_group('TofGate_'+self.gateName)   
        
        grp.create_dataset('gateInfo_tofs_tofl_tofbin', data=np.array([self.tofs,self.tofl,self.tofbin]))  
        
        for histname in self.parent.hist_names_tof:   
            try:
                grp.create_dataset(histname,data = self.hists_tof_all[histname])    
            except Exception as e:
                print(histname+' failed to be saved.')
                print(e)  


    def reduce(self):
        for histname in self.parent.hist_names_tof:  
            try:
                self.time_a = time.time()         
                MPI.COMM_WORLD.Reduce(self.hists_tof[histname],self.hists_tof_all[histname])   
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
    
