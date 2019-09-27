#Adapted from OnDA's processing script.

import time
import sys
import zmq
import numpy
import numpy as np
#import bisect

import matplotlib.pyplot as plt

from lib.onda.utils import (
    global_params as gp,
    zmq_monitor_utils as zmq_mon,
    dynamic_import as dyn_imp
)



from ImgAlgos.PyAlgos import PyAlgos


from processing_layer.algorithms.AcqirisPeakFinder import AcqirisPeakFinder
from processing_layer.algorithms.BasicHitFinder import BasicHitFinder  


par_layer = dyn_imp.import_layer_module('parallelization_layer', gp.monitor_params)

MasterWorker = getattr(par_layer, 'MasterWorker')


class Onda(MasterWorker):

    def __init__(self, source, monitor_params):

        super(Onda, self).__init__(map_func=self.process_data,
                                   reduce_func=self.collect_data,
                                   source=source, monitor_params=monitor_params)
        

        import psana


        self.npix_min, self.npix_max= monitor_params['Opal']['npix_min'],monitor_params['Opal']['npix_max']
        self.amax_thr, self.atot_thr, self.son_min = monitor_params['Opal']['amax_thr'], monitor_params['Opal']['atot_thr'], monitor_params['Opal']['son_min']
        self.thr_low, self.thr_high  = monitor_params['Opal']['thr_low'], monitor_params['Opal']['thr_high']
        self.rank, self.r0, self.dr = monitor_params['Opal']['rank'], monitor_params['Opal']['r0'], monitor_params['Opal']['dr']
        
        self.e_center_x, self.e_center_y = monitor_params['Opal']['e_center_x'],monitor_params['Opal']['e_center_y']        
        
        print 'coin_point1'
        self.params_gen = monitor_params['General']
        self.params_peakfinder_t, self.params_peakfinder_x, self.params_peakfinder_y = monitor_params['PeakFinderMcp'], monitor_params['PeakFinderX'], monitor_params['PeakFinderY']
        self.params_hitfinder = monitor_params['HitFinder']
        
        self.output_params = monitor_params['OutputLayer']
        
        self.offset_acq = [0.01310443,0.02252858,0.02097541,0.01934959,-0.0001188]   

        self.t_channel = monitor_params['DetectorLayer']['mcp_channel']
        self.x1_channel = monitor_params['DetectorLayer']['x1_channel']
        self.x2_channel = monitor_params['DetectorLayer']['x2_channel']
        self.y1_channel = monitor_params['DetectorLayer']['y1_channel']
        self.y2_channel = monitor_params['DetectorLayer']['y2_channel']
        
  #################################################################              
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
        
        
        
        self.eXmin, self.eYmin, self.eRmin, self.eAmin = monitor_params['OutputLayer']['exmin'],monitor_params['OutputLayer']['eymin'],monitor_params['OutputLayer']['ermin'],monitor_params['OutputLayer']['eamin']
        self.eXmax, self.eYmax, self.eRmax, self.eAmax = monitor_params['OutputLayer']['exmax'],monitor_params['OutputLayer']['eymax'],monitor_params['OutputLayer']['ermax'],monitor_params['OutputLayer']['eamax']
        self.eXbin, self.eYbin, self.eRbin, self.eAbin = monitor_params['OutputLayer']['exbin'],monitor_params['OutputLayer']['eybin'],monitor_params['OutputLayer']['erbin'],monitor_params['OutputLayer']['eabin']
        
        
        self.photon_eng_bin, self.pulse_eng_bin = monitor_params['OutputLayer']['photon_eng_bin'],monitor_params['OutputLayer']['pulse_eng_bin']
        self.photon_eng_min, self.pulse_eng_min = monitor_params['OutputLayer']['photon_eng_min'],monitor_params['OutputLayer']['pulse_eng_min']
        self.photon_eng_max, self.pulse_eng_max = monitor_params['OutputLayer']['photon_eng_max'],monitor_params['OutputLayer']['pulse_eng_max']        
        
        self.photon_eng_binnum = int((self.photon_eng_max - self.photon_eng_min)/self.photon_eng_bin)
        self.pulse_eng_binnum = int((self.pulse_eng_max - self.pulse_eng_min)/self.pulse_eng_bin) 
        
        self.photon_eng_axis  = np.linspace(self.photon_eng_min, self.photon_eng_max, self.photon_eng_binnum)
        self.pulse_eng_axis = np.linspace(self.pulse_eng_min, self.pulse_eng_max, self.pulse_eng_binnum)               
        
        self.eXbinnum = int((self.eXmax - self.eXmin)/self.eXbin)
        self.eYbinnum = int((self.eYmax - self.eYmin)/self.eYbin)
        self.eAbinnum = int((self.eAmax - self.eAmin)/self.eAbin)
        self.eRbinnum = int((self.eRmax - self.eRmin)/self.eRbin)    
        print 'binnum:', self.eXbinnum, self.eYbinnum
        
        self.eXaxis  = np.linspace(self.eXmin, self.eXmax, self.eXbinnum)
        self.eYaxis = np.linspace(self.eYmin, self.eYmax, self.eYbinnum)
        self.eAaxis = np.linspace(self.eAmin, self.eAmax, self.eAbinnum)
        self.eRaxis = np.linspace(self.eRmin, self.eRmax, self.eRbinnum)        
        
        self.eXaxis_r  = self.eXaxis[::-1]
        self.eYaxis_r = self.eYaxis[::-1]
        self.eAaxis_r = self.eAaxis[::-1]
        self.eRaxis_r = self.eRaxis[::-1]        
 
        self.eXaxisM = (self.eXaxis[:-1] + self.eXaxis[1:])/2
        self.eYaxisM = (self.eYaxis[:-1] + self.eYaxis[1:])/2
        self.eAaxisM = (self.eAaxis[:-1] + self.eAaxis[1:])/2        
        self.eRaxisM = (self.eRaxis[:-1] + self.eRaxis[1:])/2               

        self.pho_pls_eng = np.zeros([self.photon_eng_binnum-1 , self.pulse_eng_binnum-1])
     
        
        self.eXY = np.zeros([self.photon_eng_binnum-1 , self.pulse_eng_binnum-1, self.eXbinnum-1, self.eYbinnum-1])
        self.eAR = np.zeros([self.photon_eng_binnum-1 , self.pulse_eng_binnum-1, self.eAbinnum-1, self.eRbinnum-1])
        self.eA = np.zeros([self.photon_eng_binnum-1 , self.pulse_eng_binnum-1, self.eAbinnum-1])                     
        self.eR = np.zeros([self.photon_eng_binnum-1 , self.pulse_eng_binnum-1, self.eRbinnum-1])                                   


        self.PeakFinderT = AcqirisPeakFinder(self.params_peakfinder_t)
        self.PeakFinderX = AcqirisPeakFinder(self.params_peakfinder_x)
        self.PeakFinderY = AcqirisPeakFinder(self.params_peakfinder_y)



        self.hit_list = []

        self.HitFinder = BasicHitFinder(self.params_hitfinder)
        
        self.num_events_all = 0
        self.mask = np.ones([1024,1024])
        self.mask[350:650, 350:650] = 0
        self.mask[:, :350] = 0        

        self.alg = PyAlgos()        
        self.alg.set_peak_selection_pars(npix_min=self.npix_min, npix_max=self.npix_max, amax_thr=self.amax_thr, atot_thr=self.atot_thr, son_min=self.son_min)        


        if self.role == 'master':
            
            self.collected_data = {}
            self.publish_ip = self.params_gen['publish_ip']
            self.publish_port = self.params_gen['publish_port']
            self.speed_rep_int = self.params_gen['speed_report_interval']

            self.accumulated_shots = self.params_gen['accumulated_shots']
            self.peaks_to_send_string = self.params_gen['peaks_to_send'].split(',')
            self.peaks_to_send = (int(self.peaks_to_send_string[0]),
                                  int(self.peaks_to_send_string[1]))

            print('Starting the monitor...')
            sys.stdout.flush()


            zmq_mon.init_zmq_to_gui(self, self.publish_ip, self.publish_port)
            
            self.num_events = 0
            self.old_time = time.time()

            self.time = None

            self.data_accumulator = []


        if self.role == 'worker':
        
            self.XYw = np.zeros([self.Xbinnum-1, self.Ybinnum-1])
            self.eXYw = np.zeros([self.eXbinnum-1, self.eYbinnum-1])        
            self.eARw = np.zeros([self.eAbinnum-1, self.eRbinnum-1])            
            self.eRw = np.zeros([1, self.eRbinnum-1])            
            self.eAw = np.zeros([1, self.eAbinnum-1])                                                    
            self.Tofw = np.zeros([1, self.Tbinnum-1])                
            self.XTw = np.zeros([self.Tbinnum-1, self.Xbinnum-1])
            self.YTw = np.zeros([self.Tbinnum-1, self.Ybinnum-1])
            self.TSumXw = np.zeros([self.Tbinnum-1,1])
            self.TSumYw = np.zeros([self.Tbinnum-1,1])
        
            self.PiPiCow = np.zeros([self.Tbinnum-2,self.Tbinnum-2])        
                
            
            self.results_dict = {}

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
    
        self.results_dict = {} 
        MCPinds = [] 
        Tofinds = []
        Xinds = []
        Yinds =[]
        eXinds = []
        eYinds = []
        eAinds = []
        eRinds = []
        eXinds_f = []
        eYinds_f = []
        eAinds_f = []
        eRinds_f = []        
        
        pulse_eng_ind = 0
        photon_eng_ind = 0
 

        self.acqiris_data_wf[2:7] = self.acqiris_data_wf[2:7] - np.mean(self.acqiris_data_wf[2:7,self.acqiris_data_wt[6,:]>10000], axis=1)[:,np.newaxis]
        self.acqiris_data_wf[self.t_channel] = -self.acqiris_data_wf[self.t_channel]
        t_peaks = np.array(self.PeakFinderT.cfd(self.acqiris_data_wf[self.t_channel],self.acqiris_data_wt[self.t_channel]))
        x1_peaks = np.array(self.PeakFinderX.cfd(self.acqiris_data_wf[self.x1_channel],self.acqiris_data_wt[self.x1_channel]))
        x2_peaks = np.array(self.PeakFinderX.cfd(self.acqiris_data_wf[self.x2_channel],self.acqiris_data_wt[self.x2_channel]))
        y1_peaks = np.array(self.PeakFinderY.cfd(self.acqiris_data_wf[self.y1_channel],self.acqiris_data_wt[self.y1_channel]))
        y2_peaks = np.array(self.PeakFinderY.cfd(self.acqiris_data_wf[self.y2_channel],self.acqiris_data_wt[self.y2_channel]))
        
        
        e_peaks = self.alg.peak_finder_v4r2(self.eImage, thr_low=self.thr_low, thr_high=self.thr_high, rank=self.rank, r0=self.r0, dr=self.dr)
        
        self.num_events_all += 1
        
        if (0==1) and self.num_events_all == 60:
            self.results_dict['acq'] = (self.acqiris_data_wt, self.acqiris_data_wf)
            self.results_dict['t_peaks'] = t_peaks
            self.results_dict['x1_peaks'] = x1_peaks
            self.results_dict['x2_peaks'] = x2_peaks
            self.results_dict['y1_peaks'] = y1_peaks
            self.results_dict['y2_peaks'] = y2_peaks
        else:
            self.results_dict['acq'] = None



        
        for t_peak in t_peaks:
            MCPinds.append(next((MCP_ind for MCP_ind, MCP_ele in enumerate(self.Taxis) if MCP_ele > t_peak),0))
     
        ion_hits = self.HitFinder.FindHits(t_peaks, x1_peaks, x2_peaks, y1_peaks, y2_peaks)
        
        if (0==1):
            self.results_dict['ion_hits'] = ion_hits
        
        eXs = e_peaks[:,1].astype(int)
        eYs = e_peaks[:,2].astype(int)
        eRadius, eAngle =self.cart2polar(eXs, eYs)
        
        
        
        
        
        for ion_hit in ion_hits:
            Tofinds.append(next((Tof_ind for Tof_ind, Tof_ele in enumerate(self.Taxis) if Tof_ele > ion_hit[0]),0))
            Xinds.append(next((X_ind for X_ind, X_ele in enumerate(self.Xaxis) if X_ele > ion_hit[1]),0))
            Yinds.append(next((Y_ind for Y_ind, Y_ele in enumerate(self.Yaxis) if Y_ele > ion_hit[2]),0))
            
            
        for e_ind in range(len(eXs)):

            tempRind = next((eR_ind for eR_ind, eR_ele in enumerate(self.eRaxis) if eR_ele > eRadius[e_ind]),0)
            tempAind = next((eA_ind for eA_ind, eA_ele in enumerate(self.eAaxis) if eA_ele > eAngle[e_ind]),0)
            tempXind = next((eX_ind for eX_ind, eX_ele in enumerate(self.eXaxis) if eX_ele > eXs[e_ind]),0)
            tempYind = next((eY_ind for eY_ind, eY_ele in enumerate(self.eYaxis) if eY_ele > eYs[e_ind]),0)
            eRinds.append(tempRind)
            eAinds.append(tempAind)
            eXinds.append(tempXind)
            eYinds.append(tempYind)            
            
            if not (eRadius[e_ind] > 172.2 and eRadius[e_ind] < 361 and eAngle[e_ind] > -2.5 and eAngle[e_ind] < -0.8):         
                if eRadius[e_ind] > 100:
                    eRinds_f.append(tempRind)
                    eAinds_f.append(tempAind)
                    eXinds_f.append(tempXind)
                    eYinds_f.append(tempYind)    
                      
            

        pulse_eng_ind = next((pls_eng_ind for pls_eng_ind, pls_eng_ele in enumerate(self.pulse_eng_axis) if pls_eng_ele > self.pulse_eng),0)
        photon_eng_ind = next((pho_eng_ind for pho_eng_ind, pho_eng_ele in enumerate(self.photon_eng_axis) if pho_eng_ele > self.photon_eng),0)        
        self.results_dict['t_peaks'] = MCPinds
        self.results_dict['ion'] = {'Xinds': Xinds, 'Yinds': Yinds, 'Tofinds': Tofinds}
        self.results_dict['e'] = {'eXinds': eXinds, 'eYinds': eYinds, 'eRinds': eRinds, 'eAinds': eAinds, 'eXinds_f': eXinds_f, 'eYinds_f': eYinds_f, 'eRinds_f': eRinds_f, 'eAinds_f': eAinds_f}
        
        self.results_dict['beam'] = {'pulse_eng_ind': pulse_eng_ind, 'photon_eng_ind': photon_eng_ind}
        
   
        
        
        return self.results_dict, self.mpi_rank

    def collect_data_offline(self, new):
    
                                                                                                                                                                       

        self.collected_data = {}

        self.collected_data, _ = new         
                
        if len(self.collected_data['ion']['Xinds']) > 0 and len(self.collected_data['e']['Xinds']) > 0 and len(self.collected_data['beam']['pulse_eng_ind']) > 0 and len(self.collected_data['beam']['photon_eng_ind']) > 0:
            




        self.num_events += 1

        if self.num_events % self.speed_rep_int == 0:
            self.time = time.time()
            print('Processed: {0} in {1:.2f} seconds ({2:.2f} Hz)'.format(
                self.num_events,
                self.time - self.old_time,
                float(self.speed_rep_int)/float(self.time-self.old_time)))
            sys.stdout.flush()
            self.old_time = self.time

        if self.num_events == self.output_params['max_events'] :

            
            self.shutdown(msg='maximum number of events reached.')

        return
        
        

    def collect_data(self, new):
    
                                                                                                                                                                       

        self.collected_data = {}

        self.collected_data, _ = new
        
 
        
        
        if len(self.collected_data['ion']['Xinds']) > 0 and len(self.collected_data['e']['Xinds']) > 0 and len(self.collected_data['beam']['pulse_eng_ind']) > 0 and len(self.collected_data['beam']['photon_eng_ind']) > 0:
            
            self.zmq_publish.send(b'coin_data', zmq.SNDMORE)
            self.zmq_publish.send_pyobj(self.collected_data)


        self.num_events += 1

        if self.num_events % self.speed_rep_int == 0:
            self.time = time.time()
            print('Processed: {0} in {1:.2f} seconds ({2:.2f} Hz)'.format(
                self.num_events,
                self.time - self.old_time,
                float(self.speed_rep_int)/float(self.time-self.old_time)))
            sys.stdout.flush()
            self.old_time = self.time

        if self.num_events == self.output_params['max_events'] :


            
            self.shutdown(msg='maximum number of events reached.')

        return
