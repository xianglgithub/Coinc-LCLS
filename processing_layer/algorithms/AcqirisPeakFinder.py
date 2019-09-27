
import numpy as np
from scipy.optimize import bisect
#from psana import *

class AcqirisPeakFinder:

    def __init__(self, params):
        self.sample_interval = params['sample_interval']
        self.delay = int(params['delay']/self.sample_interval)
        self.fraction = params['fraction']
        self.threshold = params['threshold']
        self.walk = params['walk']
        self.polarity = 1 if params['polarity']=='Positive' else -1
        self.timerange_low = params['timerange_low']
        self.timerange_high = params['timerange_high']
                
        
        
    def NewtonPolynomial3(self,x,x_arr,y_arr):
    
        d_0_1 = (y_arr[1] - y_arr[0])/(x_arr[1] - x_arr[0])
        d_1_2 = (y_arr[2] - y_arr[1])/(x_arr[2] - x_arr[1])
        d_2_3 = (y_arr[3] - y_arr[2])/(x_arr[3] - x_arr[2])
        
        d_0_1_2 = (d_1_2 - d_0_1)/(x_arr[2] - x_arr[0])
        d_1_2_3 = (d_2_3 - d_1_2)/(x_arr[3] - x_arr[1])        
        d_0_1_2_3 = (d_1_2_3 - d_0_1_2)/(x_arr[3] - x_arr[0])
        
        c0 = y_arr[0]
        c1 = d_0_1
        c2 = d_0_1_2
        c3 = d_0_1_2_3
        
        return c0 + c1*(x-x_arr[0]) + c2*(x-x_arr[0])*(x-x_arr[1]) + c3*(x-x_arr[0])*(x-x_arr[1])*(x-x_arr[2])
        
            
    def cfd(self,wf, wt):
        
        wf = wf[(wt>self.timerange_low)&(wt<self.timerange_high)]
        wt = wt[(wt>self.timerange_low)&(wt<self.timerange_high)]
        
        
        wf_1 = wf[:-self.delay]
        wf_2 = wf[self.delay:]
       
        wf_cal = wf_1 - self.fraction*wf_2      
        wf_cal_m_walk = self.polarity*wf_cal-self.walk
        wf_cal_m_walk_sign = np.sign(wf_cal_m_walk)
      #  wf_cal_sign_1 = wf_cal_sign[:-1]
      #  wf_cal_sign_2 = wf_cal_sign[1:]
        wf_cal_ind = np.where((wf_cal_m_walk_sign[:-1] < wf_cal_m_walk_sign[1:]) & 
        (wf_cal_m_walk_sign[1:] != 0) & ((wf_cal_m_walk[1:] - wf_cal_m_walk[:-1]) >= 1e-8))[0] 
      #  print '1: ',wf_cal_ind, len(wf_cal_ind)
    #    wf_cal_ind_ind = np.where(self.polarity*wf_2[wf_cal_ind] > self.threshold)[0]
#correction
        wf_cal_ind_ind = np.where(self.polarity*wf_1[wf_cal_ind] > self.threshold)[0]

        


        
      #  print '2: ',len(wf_cal_ind_ind)
        t_cfd_list = []
        
        for ind in wf_cal_ind_ind:
#            print '2: ',ind,wf_cal_ind_ind, type(wf_cal_ind_ind)
#            print '3: ',(wf_cal_ind[0][ind]+self.delay-1), (wf_cal_ind[0][ind]+self.delay+3)
#            t_arr = wt[(wf_cal_ind[ind]+self.delay-1):(wf_cal_ind[ind]+self.delay+3)]
#correction
            t_arr = wt[(wf_cal_ind[ind]-1):(wf_cal_ind[ind]+3)]

            wf_cal_m_walk_arr = wf_cal_m_walk[(wf_cal_ind[ind]-1):(wf_cal_ind[ind]+3)]
            
            #change
            if len(t_arr) != 4 or len(wf_cal_m_walk_arr) != 4:
                continue
            #change
            
            if (t_arr[1] - t_arr[0])==0 or (t_arr[2] - t_arr[1])==0 or (t_arr[3] - t_arr[2])==0:
                continue
                
            if (t_arr[2] - t_arr[0])==0 or (t_arr[3] - t_arr[1])==0 or (t_arr[3] - t_arr[0])==0:
                continue
            
            t_cfd = bisect(self.NewtonPolynomial3,t_arr[1],t_arr[2],args=(t_arr, wf_cal_m_walk_arr),xtol=1e-3)
            
            if t_cfd>self.timerange_low and t_cfd<self.timerange_high:
                t_cfd_list.append(t_cfd)
    #            t_cfd_list.append(t_arr[1])
                
      #  print 'changed'
                
        return t_cfd_list
