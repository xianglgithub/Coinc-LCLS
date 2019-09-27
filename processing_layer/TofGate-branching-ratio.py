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
    def __init__(self, parent, gateName, tofs, tofl,tofs_dict,tofl_dict):
        self.parent = parent
        self.gateName = gateName
        self.tofs = tofs
        self.tofl = tofl
        self.tofs_dict = tofs_dict
        self.tofl_dict = tofl_dict
        self.tofbin = self.parent.monitor_params['t']['bin']
        
        print self.tofs_dict,self.tofl_dict
        self.tof_ind = (self.parent.TaxisM>self.tofs) & (self.parent.TaxisM<self.tofl)
        

        self.particle = self.gateName
        
        self.extractE = extractE
        
        self.alg = PyAlgos()        
        self.alg.set_peak_selection_pars(npix_min=self.parent.npix_min, npix_max=self.parent.npix_max, amax_thr=self.parent.amax_thr, atot_thr=self.parent.atot_thr, son_min=self.parent.son_min)           
        
        self.init_vars()
    
    def init_vars(self):
    
    

        self.P = {}     
        for pt in ['2n1','n1','n2','n3','n4']:
            self.P[pt] = 0
        
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

            if hist_name == 'frag_stat':
                     
                x_name = self.parent.monitor_params[hist_name]['x']
                x_binnum = self.parent.monitor_params[x_name]['num']   
                     
                y_name = self.parent.monitor_params[hist_name]['y']
                y_binnum = self.parent.monitor_params[y_name]['num']  
                
                z_name = self.parent.monitor_params[hist_name]['z']
                z_binnum = self.parent.monitor_params[z_name]['num']   
                
                m_name = self.parent.monitor_params[hist_name]['m']
                m_binnum = self.parent.monitor_params[m_name]['num']
                
                n_name = self.parent.monitor_params[hist_name]['n']
                n_binnum = self.parent.monitor_params[n_name]['num']                
                                             
                self.hists_tof[hist_name] = np.zeros([x_binnum, y_binnum, z_binnum, m_binnum, n_binnum])                      
                if self.parent.role == 'master':
                    self.hists_tof_all[hist_name] = np.zeros([x_binnum, y_binnum, z_binnum, m_binnum, n_binnum])  
                else:
                    self.hists_tof_all[hist_name] = None   
                continue
                               
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
            
        pass
                   
         
        
    def update_ion(self,Tofele, Xele, Yele):
        
        for pt in ['2n1','n1','n2','n3','n4']:
            if (Tofele > self.tofs_dict[pt] and Tofele < self.tofl_dict[pt]):   
             #   if self.parent.mpi_rank == 0: 
             #       print pt, Tofele                
                self.P[pt] += 1    
                break
  

            
        
            
              
        
    def is_coin(self):
      #  a = 0
      #  for pt in ['2n1','n1','n2','n3','n4']:
      #      a += self.P[pt]
     
        return True 
                        
        
                
    def update_shotinfo(self, pho_ind, pls_ind):   
    
   #     if self.parent.mpi_rank == 0:  
   #         print 'Tof***********************update',self.P                     
        self.hists_tof['frag_stat'][min(self.P['2n1'],9),min(self.P['n1'],9),min(self.P['n2'],9),min(self.P['n3'],9),min(self.P['n4'],9)] += 1          

            
                  
        
        
           
        
    def reset_coin_var(self):
            
    #    if self.parent.mpi_rank == 0: 
    #        print 'Tof**********************reset',self.P     
        for pt in ['2n1','n1','n2','n3','n4']:
            self.P[pt] = 0
    #    if self.parent.mpi_rank == 0: 
    #        print 'Tof**********************afterreset',self.P             
            

  
                
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

  
    
