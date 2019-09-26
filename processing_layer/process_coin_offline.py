import time
import sys
import zmq
import numpy
import numpy as np
import h5py

from mpi4py import MPI

import matplotlib.pyplot as plt

from lib.onda.utils import (
    global_params as gp,
    zmq_monitor_utils as zmq_mon,
    dynamic_import as dyn_imp
)



from ImgAlgos.PyAlgos import PyAlgos


from processing_layer.algorithms.AcqirisPeakFinder import AcqirisPeakFinder
from processing_layer.algorithms.BasicHitFinder import BasicHitFinder  

from PiPiCoGate import PiPiCoGate
from TofGate import TofGate
from MCPGate import MCPGate


par_layer = dyn_imp.import_layer_module('parallelization_layer', gp.monitor_params)

Workers = getattr(par_layer, 'Workers')


class Coin(Workers):

    def init_params(self,monitor_params):
    
        
        self.npix_min, self.npix_max= monitor_params['Opal']['npix_min'],monitor_params['Opal']['npix_max']
        self.amax_thr, self.atot_thr, self.son_min = monitor_params['Opal']['amax_thr'], monitor_params['Opal']['atot_thr'], monitor_params['Opal']['son_min']
        self.thr_low, self.thr_high  = monitor_params['Opal']['thr_low'], monitor_params['Opal']['thr_high']
        self.rank, self.r0, self.dr = monitor_params['Opal']['rank'], monitor_params['Opal']['r0'], monitor_params['Opal']['dr']
        
        self.eimg_center_x, self.eimg_center_y = monitor_params['Opal']['eimg_center_x'],monitor_params['Opal']['eimg_center_y']   
        self.e_radius = monitor_params['Opal']['e_radius'] 
        
        self.params_gen = monitor_params['General']



        
        
        self.output_path = monitor_params['OutputLayer']['output_path']   
        
           
                      
        
  #################################################################   
        self.output_params = monitor_params['OutputLayer']
        
        self.vars = monitor_params['OutputLayer']['vars'].split(',')       
        self.hist_names_all = monitor_params['OutputLayer']['hist_names_all'].split(',')      
        
        self.hist1_names_all = monitor_params['OutputLayer']['hist1_names_all'].split(',')                  
     
        #self.vars_min = {}; self.vars_max = {}; self.vars_bin= {}; 
        self.vars_binnum = {}; self.vars_axis={}
        self.hists_all = {}    
        self.hists_all_all = {}                           
                       
        
        for var in self.vars:
            var_min= monitor_params[var]['min']
            var_max = monitor_params[var]['max']
            var_bin = monitor_params[var]['bin']  
            var_binnum = int((var_max - var_min)/var_bin)+1
            self.vars_binnum[var] = var_binnum
            self.vars_axis[var] = np.linspace(var_min, var_max, var_binnum)

        for hist_name in self.hist_names_all:
            if hist_name=='pipico':
                x_name = self.monitor_params[hist_name]['x']
                x_binnum = self.vars_binnum[x_name]        
                y_name = self.monitor_params[hist_name]['y']
                y_binnum = self.vars_binnum[y_name]                    
                self.hists_all[hist_name] = np.zeros([x_binnum-2, y_binnum-2])      
                if self.role == 'master':
                    self.hists_all_all[hist_name] = np.zeros([x_binnum-2, y_binnum-2]) 
                else:
                    self.hists_all_all[hist_name] = None   
                continue

                               
            x_name = self.monitor_params[hist_name]['x']
            x_binnum = self.vars_binnum[x_name]
            if 'y' in self.monitor_params[hist_name].keys():
                y_name = self.monitor_params[hist_name]['y']
                y_binnum = self.vars_binnum[y_name]
                if 'z' in self.monitor_params[hist_name].keys():
                    z_name = self.monitor_params[hist_name]['z']
                    z_binnum = self.vars_binnum[z_name] 
                    self.hists_all[hist_name] = np.zeros([x_binnum-1, y_binnum-1, z_binnum-1])
                    if self.role == 'master':
                        self.hists_all_all[hist_name] = np.zeros([x_binnum-1, y_binnum-1, z_binnum-1])
                    else:
                        self.hists_all_all[hist_name] = None
                    
                else:
                    self.hists_all[hist_name] = np.zeros([x_binnum-1, y_binnum-1])     
                    if self.role == 'master':
                        self.hists_all_all[hist_name] = np.zeros([x_binnum-1, y_binnum-1])
                    else:
                        self.hists_all_all[hist_name] = None                        
            else:
                self.hists_all[hist_name] = np.zeros([x_binnum-1])
                if self.role == 'master':
                    self.hists_all_all[hist_name] = np.zeros([x_binnum-1])
                else:
                    self.hists_all_all[hist_name] = None  
          #  print self.hists_all[hist_name].dtype,self.hists_all_all[hist_name].dtype
                     
                    
        for hist1_name in self.hist1_names_all:
         #   print 'hist1_name',hist1_name
            self.hists_all[hist1_name] = np.array([0],dtype=np.float64)
            if self.role == 'master':
                self.hists_all_all[hist1_name] = np.array([0],dtype=np.float64)  
            else:
                self.hists_all_all[hist1_name] = None  
            self.hist_names_all.append(hist1_name)   
          #  print self.hists_all[hist_name].dtype,self.hists_all_all[hist_name].dtype
        
                            
        
                    
        
            

    def __init__(self, source, monitor_params):

        super(Coin, self).__init__(map_func=self.process_data,
                                   reduce_func=self.reduce,save_func=self.save_data,
                                   source=source, monitor_params=monitor_params)
        
        

        import psana
 
        self.monitor_params = monitor_params
        self.init_params(monitor_params)
        
        self.e_cols = self.eimg_center_y - self.e_radius     
        self.e_coll = self.eimg_center_y + self.e_radius+1   
        
        self.e_rows = self.eimg_center_x - self.e_radius     
        self.e_rowl = self.eimg_center_x + self.e_radius+1         
        
        self.e_center_y = self.eimg_center_y
        self.e_center_x = self.eimg_center_x          
        
                                            
        

        self.mask = np.ones([1024,1024])
        self.mask[350:650, 350:650] = 0
        self.mask[:, :350] = 0        
        
        #self.alg = PyAlgos(mask = self.mask)
        self.alg = PyAlgos()        
        self.alg.set_peak_selection_pars(npix_min=self.npix_min, npix_max=self.npix_max, amax_thr=self.amax_thr, atot_thr=self.atot_thr, son_min=self.son_min)        




        self.speed_rep_int = self.params_gen['speed_report_interval']


        self.old_time = time.time()

        self.time = None



        print('Starting worker: {0}.'.format(self.mpi_rank))
        sys.stdout.flush()

        return

        
    def cart2polar_img(self, x, y, intensity):
    
        x1 = x-self.e_center_x
        y1 = y-self.e_center_y
        r = np.sqrt(x1**2 + y1**2)

        angle = np.arctan2(y1, x1)
        return r, angle, intensity*r    
        
    def cart2polar(self, x, y):
    
        x1 = x-self.e_center_x
        y1 = y-self.e_center_y
        r = np.sqrt(x1**2 + y1**2)

        angle = np.arctan2(y1, x1)
        return r, angle         



    def process_data(self):
    
        
        self.pls_ind = next((pls_eng_ind for pls_eng_ind, pls_eng_ele in enumerate(self.vars_axis['plseng']) if pls_eng_ele > self.pulse_eng),0)-1
        self.pho_ind = next((pho_eng_ind for pho_eng_ind, pho_eng_ele in enumerate(self.vars_axis['phoeng']) if pho_eng_ele > self.photon_eng),0)-1       
        self.ebm_ind = next((ebm_eng_ind for ebm_eng_ind, ebm_eng_ele in enumerate(self.vars_axis['ebmeng']) if ebm_eng_ele > self.ebeam_eng),0)-1 
                           
       # self.hists_all['num_events'][0] += 1          
        if (self.ebm_ind != -1 and self.pls_ind != -1):

            self.sortDataE(self.ebm_ind)
                            
                               
            self.hists_all['ebm_pls_eng'][self.ebm_ind, self.pls_ind] += 1   
            if self.pho_ind != -1:  
                self.hists_all['ebm_pho_eng'][self.ebm_ind, self.pho_ind] += 1 
                

            self.hists_all['num_events'][0] += 1  
            

     #   print self.mpi_rank, self.hists_all['num_events'][0] 


        if self.role == 'master' and (self.hists_all['num_events'][0]*self.mpi_size) % self.speed_rep_int == 0:
            self.time = time.time()
            print('Processed: {0} in {1:.2f} seconds ({2:.2f} Hz)'.format(
                self.mpi_size*self.hists_all['num_events'][0],
                self.time - self.old_time,
                float(self.speed_rep_int)/float(self.time-self.old_time)))
            sys.stdout.flush()
            self.old_time = self.time

        if self.role == 'master' and self.mpi_size*self.hists_all['num_events'][0] == self.output_params['max_events'] :
            self.save_data()
          
            self.shutdown(msg='maximum number of events reached.')


        return 
        
        

        
 
    def sortDataE(self,ebm_ind):
          
        e_peaks = self.alg.peak_finder_v4r2(self.eImage, thr_low=self.thr_low, thr_high=self.thr_high, rank=self.rank, r0=self.r0, dr=self.dr)
        
        eXs = e_peaks[:,1].astype(int)
        eYs = e_peaks[:,2].astype(int)
        eRadius, eAngle =self.cart2polar(eXs, eYs)

        for e_ind in range(len(eXs)):

            tempXind = next((eX_ind for eX_ind, eX_ele in enumerate(self.vars_axis['ex']) if eX_ele > eXs[e_ind]),0)-1
            tempYind = next((eY_ind for eY_ind, eY_ele in enumerate(self.vars_axis['ey']) if eY_ele > eYs[e_ind]),0)-1

            if tempXind != -1 and tempYind != -1:    

                self.hists_all['ebm_ex_ey'][ebm_ind,tempXind, tempYind] += 1



            
    def sortDataIon(self):
    
        self.tof_inds = []
   
        self.acqiris_data_wf[2:7] = self.acqiris_data_wf[2:7] - np.mean(self.acqiris_data_wf[2:7,self.acqiris_data_wt[6,:]>8000], axis=1)[:,np.newaxis]
        #self.acqiris_data_wf[self.t_channel] = -self.acqiris_data_wf[self.t_channel]
        t_peaks = np.array(self.PeakFinderT.cfd(self.acqiris_data_wf[self.t_channel],self.acqiris_data_wt[self.t_channel]))        
        if len(t_peaks) > 0:        
           # for t_peak in t_peaks:
            #    tempMCPind = next((MCP_ind for MCP_ind, MCP_ele in enumerate(self.vars_axis['t']) if MCP_ele > t_peak),0)-1
           #     if tempMCPind != -1:
          #          self.MCPTof[tempMCPind] += 1                 
         #           self.updateMCPGatesIon(tempMCPind)                                  
                                   
            x1_peaks = np.array(self.PeakFinderX.cfd(self.acqiris_data_wf[self.x1_channel],self.acqiris_data_wt[self.x1_channel]))
            x2_peaks = np.array(self.PeakFinderX.cfd(self.acqiris_data_wf[self.x2_channel],self.acqiris_data_wt[self.x2_channel]))
            y1_peaks = np.array(self.PeakFinderY.cfd(self.acqiris_data_wf[self.y1_channel],self.acqiris_data_wt[self.y1_channel]))
            y2_peaks = np.array(self.PeakFinderY.cfd(self.acqiris_data_wf[self.y2_channel],self.acqiris_data_wt[self.y2_channel]))        
            
        # [(mcp_peak, (x, y,), (x1, x2, y1, y2)), ...]
            ion_hits = self.HitFinder.FindHits(t_peaks, x1_peaks, x2_peaks, y1_peaks, y2_peaks)
        
            for ion_hit in ion_hits:
                tempTofind = next((Tof_ind for Tof_ind, Tof_ele in enumerate(self.vars_axis['t']) if Tof_ele > ion_hit[0]),0)-1
                tempXind = next((X_ind for X_ind, X_ele in enumerate(self.vars_axis['x']) if X_ele > ion_hit[1]),0)-1
                tempYind = next((Y_ind for Y_ind, Y_ele in enumerate(self.vars_axis['y']) if Y_ele > ion_hit[2]),0)-1
                if tempTofind != -1 and tempXind != -1 and tempYind != -1:                  
        
                    self.tof_inds.append(tempTofind)
            
                    self.hists_all['t_'][tempTofind] += 1
                    self.hists_all['x_y'][tempXind, tempYind] += 1
                 #   self.XT[tempTofind, tempXind] += 1
                 #   self.YT[tempTofind, tempYind] += 1  
                
                
                
                    self.updateTofGatesIon(tempTofind, tempXind, tempYind, ion_hit[0], ion_hit[1], ion_hit[2])
                    self.updatePiPiCoGatesIon(tempTofind, tempXind, tempYind, ion_hit[0], ion_hit[1], ion_hit[2])   
                
            self.tof_inds = sorted(self.tof_inds)    
            if len(self.tof_inds) > 1:
                for i_tof_ind in range(len(self.tof_inds)-1):
             #   print '****************************************',self.PiPiCo.shape, len(self.tof_inds)
                    self.hists_all['pipico'][self.tof_inds[i_tof_ind],self.tof_inds[(i_tof_ind+1):]]  += 1                                                             
                    
            if len(self.tof_inds) > 0:     
        
                F_sum,_  = np.histogram(self.HitFinder.F_sum, bins=self.TSum_axis)
                S_sum,_  = np.histogram(self.HitFinder.S_sum, bins=self.TSum_axis)
   
                
                self.hists_all['F_sum'] += F_sum
                self.hists_all['S_sum'] += S_sum
                        
                           

        
        
    def updateMCPGatesIon(self, t_ind):
        for M_key, M_item in self.MCPGates.iteritems():
            M_item.update_ion(t_ind)
            
    def updateTofGatesIon(self, t_ind,x_ind,y_ind,tele,xele,yele):
        for T_key, T_item in self.TofGates.iteritems():
            T_item.update_ion(t_ind, x_ind, y_ind,tele,xele,yele)            
            
    def updatePiPiCoGatesIon(self, t_ind, xind, yind,tele,xele,yele):
        for P_key, P_item in self.PiPiCoGates.iteritems():
            P_item.update_ion(t_ind, xind, yind,tele,xele,yele) 
            
    def updateMCPGatesE(self, eAind, eRind, eXind, eYind):
        for M_key, M_item in self.MCPGates.iteritems():
            if M_item.is_coin():
                M_item.update_electron(eAind, eRind, eXind, eYind)
            
    def updateTofGatesE(self, eAind, eRind, eXind, eYind):
        for T_key, T_item in self.TofGates.iteritems():
            if T_item.is_coin():
                T_item.update_electron(eAind, eRind, eXind, eYind)            
            
    def updatePiPiCoGatesE(self, eAind, eRind, eXind, eYind, pho_ind, pls_ind):
        for P_key, P_item in self.PiPiCoGates.iteritems():
            if P_item.is_coin():
                P_item.update_electron(eAind, eRind, eXind, eYind, pho_ind, pls_ind)     
                
                
    def updateShotInfo(self,phoInd, plsInd,phoEng,plsEng):
       for M_key, M_item in self.MCPGates.iteritems():
           if M_item.is_coin():
               M_item.update_shotinfo(phoInd, plsInd)  
           M_item.reset_coin_var()  
               
       for T_key, T_item in self.TofGates.iteritems():
           if T_item.is_coin():
               T_item.update_shotinfo(phoInd, plsInd)  
           T_item.reset_coin_var()     
               
       for P_key, P_item in self.PiPiCoGates.iteritems():
           if P_item.is_coin():
               P_item.update_shotinfo(phoInd, plsInd,phoEng,plsEng)    
           P_item.reset_coin_var()            
           
           
    def reduce(self):
        print(str(self.mpi_rank)+' starts reduce.')
        for histname in self.hist_names_all:
         #   self.time_a = time.time()
            try:
                self.time_a = time.time()
                MPI.COMM_WORLD.Reduce(self.hists_all[histname],self.hists_all_all[histname])  
                self.time_b = time.time() 
                print(histname+' reduced by '+'Rank {0} in {1:.2f} seconds'.format(self.mpi_rank,self.time_b - self.time_a))
            except Exception as e:
                print(histname+' failed to be redueced by '+str(self.mpi_rank))
                print(e) 
         #   self.time_b = time.time()  
         #   print(histname+' reduced by '+'Rank {0} in {1:.2f} seconds'.format(self.mpi_rank,self.time_b - self.time_a))
          
                            
        
        
    def save_data(self,num_lost_events_timecond,num_lost_events_datacond,num_lost_events_evtcond,num_failed_events,num_reduced_events):
        print 'saving hdf5 file'
        h5f = h5py.File(self.output_path,'w')

        
        grp = h5f.create_group('all') 
        
        try:  
              
            grp.create_dataset('num_lost_events_timecond',data = num_lost_events_timecond)    
            grp.create_dataset('num_lost_events_datacond',data = num_lost_events_datacond)              
            grp.create_dataset('num_lost_events_evtcond',data = num_lost_events_evtcond)  
            grp.create_dataset('num_failed_events',data = num_failed_events)                
            grp.create_dataset('num_reduced_events',data = num_reduced_events)  
        except Exception as e:
            print('events stats'+' failed to be saved.')
            print(e) 
        
        for histname in self.hist_names_all:
            try:
                grp.create_dataset(histname,data = self.hists_all_all[histname])   
            except Exception as e:
                print(histname+' failed to be saved.')
                print(e)                                               
            
                      


        grp1 = h5f.create_group('axis') 
        
        for var in self.vars:  
            try:
                grp1.create_dataset(var+'_axis',data = self.vars_axis[var])  
            except Exception as e:
                print(var+'_axis failed to be saved.')
                print(e)                
                    
             
                                                                                                    
        h5f.close()    
        print 'saved hdf5 file'        
        
        
    def init_gates(self):
    

        self.PiPiCoGates = {}
        for PPG in range(self.PiPiCoGates_params['num_gates']):
            gateName = self.PiPiCoGates_params['gate'+str(PPG+1)+'_name'] 
            tof1s = self.PiPiCoGates_params['gate'+str(PPG+1)+'_tof1s']
            tof1l = self.PiPiCoGates_params['gate'+str(PPG+1)+'_tof1l'] 
            tof2s = self.PiPiCoGates_params['gate'+str(PPG+1)+'_tof2s']  
            tof2l = self.PiPiCoGates_params['gate'+str(PPG+1)+'_tof2l'] 
            tof3s = self.PiPiCoGates_params['gate'+str(PPG+1)+'_tof3s']  
            tof3l = self.PiPiCoGates_params['gate'+str(PPG+1)+'_tof3l']             
            thresh1_n3n1 = self.PiPiCoGates_params['gate'+str(PPG+1)+'_thresh1_n3n1']       
            thresh2_n3n1 = self.PiPiCoGates_params['gate'+str(PPG+1)+'_thresh2_n3n1']    
            thresh1_n3n2 = self.PiPiCoGates_params['gate'+str(PPG+1)+'_thresh1_n3n2']       
            thresh2_n3n2 = self.PiPiCoGates_params['gate'+str(PPG+1)+'_thresh2_n3n2']                  
            self.PiPiCoGates[gateName] = PiPiCoGate(self, gateName, tof1s, tof1l, tof2s, tof2l,tof3s, tof3l,thresh1_n3n1,thresh2_n3n1,thresh1_n3n2,thresh2_n3n2,self.ang_f)
            
      
        self.TofGates = {}
        for TofG in range(self.TofGates_params['num_gates']):
            gateName = self.TofGates_params['gate'+str(TofG+1)+'_name'] 
            tofs = self.TofGates_params['gate'+str(TofG+1)+'_tofs']
            tofl = self.TofGates_params['gate'+str(TofG+1)+'_tofl'] 
            thresh1_tof = self.TofGates_params['gate'+str(TofG+1)+'_thresh1']       
            thresh2_tof = self.TofGates_params['gate'+str(TofG+1)+'_thresh2'] 
            self.TofGates[gateName] = TofGate(self, gateName, tofs, tofl,thresh1_tof,thresh2_tof)   
            

        self.MCPGates = {}
        for MCPG in range(self.MCPGates_params['num_gates']):
            gateName = self.MCPGates_params['gate'+str(MCPG+1)+'_name'] 
            tofs = self.MCPGates_params['gate'+str(MCPG+1)+'_tofs']
            tofl = self.MCPGates_params['gate'+str(MCPG+1)+'_tofl'] 

            self.MCPGates[gateName] = MCPGate(self, gateName, tofs, tofl)     
                


