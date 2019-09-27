
import numpy as np


class BasicHitFinder:

    def __init__(self, params):
        
        self.McpRadius = params['mcp_radius']                                  #parameter initializations
        self.ExtraRuntimeFirstLayer = params['extra_runtime_firstlayer']
        self.TSumLowFirstLayer = params['tsum_low_firstlayer']
        self.TSumHighFirstLayer = params['tsum_high_firstlayer']
        self.TSumAvgFirstLayer = (self.TSumLowFirstLayer + self.TSumHighFirstLayer)/2
        self.ScaleFactorFirstLayer = params['scalefactor_firstlayer']
        self.ExtraRuntimeSecondLayer = params['extra_runtime_secondlayer']
        self.TSumLowSecondLayer = params['tsum_low_secondlayer']
        self.TSumHighSecondLayer = params['tsum_high_secondlayer']
        self.TSumAvgSecondLayer = (self.TSumLowSecondLayer + self.TSumHighSecondLayer)/2
        self.ScaleFactorSecondLayer = params['scalefactor_secondlayer']
        

    #    print 'F_calc1:',-self.TSumAvgFirstLayer + 2*self.ExtraRuntimeFirstLayer
    #    print 'F_calc2:',self.TSumAvgFirstLayer + 2*self.ExtraRuntimeFirstLayer
    #    print 'S_calc1:',-self.TSumAvgSecondLayer + 2*self.ExtraRuntimeSecondLayer
    #    print 'S_calc2:',self.TSumAvgSecondLayer + 2*self.ExtraRuntimeSecondLayer
        ##change2
        
    def FindHits(self, McpSig, F1Sig, F2Sig, S1Sig, S2Sig):
    
    
        ##change1
        self.F1_cal = np.array([])
        self.F2_cal = np.array([])
        self.S1_cal = np.array([])
        self.S2_cal = np.array([])
        self.F_sum = np.array([])
        self.S_sum = np.array([])    
    
        F1Sig_used_counter = np.zeros(len(F1Sig))        #variables for tracking how many times each of the signals were used for hit reconstruction.
        F2Sig_used_counter = np.zeros(len(F2Sig))
        S1Sig_used_counter = np.zeros(len(S1Sig))
        S2Sig_used_counter = np.zeros(len(S2Sig))
        
        Hits = []
        
     #   temp_tsum_dict = {}
               
        candid_id = 0
        candid_min_dtsum_dict = {}
        candid_sig_ind_dict = {}
        candid_hit_ind_dict = {}        
        delete_ind_list = [] 
        
#        temp_f1_tsum_dict = {}
#        temp_f2_tsum_dict = {}
#       temp_s1_tsum_dict = {}
#        temp_s2_tsum_dict = {}
        
           
             
      #  temp_f1_calc_dict = {}
      #  temp_f2_calc_dict = {}
      #  temp_s1_calc_dict = {}
      #  temp_s2_calc_dict = {}
        
        #change
    #    self.F1_cal = np.hstack([self.F1_cal,2*F1Sig - self.TSumAvgFirstLayer])
    #    self.F2_cal = np.hstack([self.F2_cal,2*F2Sig - self.TSumAvgFirstLayer])
    #    self.S1_cal = np.hstack([self.S1_cal,2*S1Sig - self.TSumAvgSecondLayer])
    #    self.S2_cal = np.hstack([self.S2_cal,2*S2Sig - self.TSumAvgSecondLayer])   
     #       
     #   self.F_sum = np.hstack([self.F_sum,np.ravel(F1Sig[:,np.newaxis] + 
     #                                                   F2Sig[np.newaxis,:])])
     #   self.S_sum = np.hstack([self.S_sum,np.ravel(S1Sig[:,np.newaxis] + 
     #                                                   S2Sig[np.newaxis,:])])
        #change
               
        for i_McpT, McpT in enumerate(McpSig):
           # print type(F1Sig), type(McpT), type()
            F1_calc = np.abs(2*F1Sig - 2*McpT - self.TSumAvgFirstLayer)
            F2_calc = np.abs(2*F2Sig - 2*McpT - self.TSumAvgFirstLayer)
            S1_calc = np.abs(2*S1Sig - 2*McpT - self.TSumAvgSecondLayer)
            S2_calc = np.abs(2*S2Sig - 2*McpT - self.TSumAvgSecondLayer)
            
            #change
            self.F1_cal = np.hstack([self.F1_cal,F1_calc])
            self.F2_cal = np.hstack([self.F2_cal,F2_calc])
            self.S1_cal = np.hstack([self.S1_cal,S1_calc])
            self.S2_cal = np.hstack([self.S2_cal,S2_calc])           
            #change
 
            #The condition below is equivalent to time sum and time difference condictions combined.
#            F1Sig_ind = np.where(((F1_calc > -self.TSumAvgFirstLayer + 2*self.ExtraRuntimeFirstLayer) &          
#            (F1_calc < self.TSumAvgFirstLayer + 2*self.ExtraRuntimeFirstLayer)))[0]
            
#            F2Sig_ind = np.where(((F2_calc > -self.TSumAvgFirstLayer + 2*self.ExtraRuntimeFirstLayer) & 
#            (F2_calc < self.TSumAvgFirstLayer + 2*self.ExtraRuntimeFirstLayer)))[0]
            
#            S1Sig_ind = np.where(((S1_calc > -self.TSumAvgSecondLayer + 2*self.ExtraRuntimeSecondLayer) & 
#            (S1_calc < self.TSumAvgSecondLayer + 2*self.ExtraRuntimeSecondLayer)))[0]
            
#            S2Sig_ind = np.where(((S2_calc > -self.TSumAvgSecondLayer + 2*self.ExtraRuntimeSecondLayer) & 
#            (S2_calc < self.TSumAvgSecondLayer + 2*self.ExtraRuntimeSecondLayer)))[0]
            
                #The condition below is equivalent to time sum and time difference condictions combined.
            F1Sig_ind = np.where(((F1_calc < self.TSumAvgFirstLayer + 2*self.ExtraRuntimeFirstLayer)))[0]
            
            F2Sig_ind = np.where(((F2_calc < self.TSumAvgFirstLayer + 2*self.ExtraRuntimeFirstLayer)))[0]
            
            S1Sig_ind = np.where(((S1_calc < self.TSumAvgSecondLayer + 2*self.ExtraRuntimeSecondLayer)))[0]
            
            S2Sig_ind = np.where(((S2_calc < self.TSumAvgSecondLayer + 2*self.ExtraRuntimeSecondLayer)))[0]
            
             
            F1F2_sum = F1Sig[F1Sig_ind][:,np.newaxis] + F2Sig[F2Sig_ind][np.newaxis,:] - 2*McpT              
            S1S2_sum = S1Sig[S1Sig_ind][:,np.newaxis] + S2Sig[S2Sig_ind][np.newaxis,:] - 2*McpT

  
            
            #change
#            self.F_sum = np.hstack([self.F_sum,np.ravel(F1Sig[:,np.newaxis] + 
#                                                        F2Sig[np.newaxis,:] - 2*McpT )])
#            self.S_sum = np.hstack([self.S_sum,np.ravel(S1Sig[:,np.newaxis] + 
#                                                        S2Sig[np.newaxis,:] - 2*McpT)])
            #change
    
            #change
            self.F_sum = np.hstack([self.F_sum,np.ravel(F1F2_sum)])
            self.S_sum = np.hstack([self.S_sum,np.ravel(S1S2_sum)])
            #change
            
            #time sum conditions
            F1Sig_ind_ind, F2Sig_ind_ind = np.where((F1F2_sum>self.TSumLowFirstLayer)&(F1F2_sum<self.TSumHighFirstLayer))  
            S1Sig_ind_ind, S2Sig_ind_ind = np.where((S1S2_sum>self.TSumLowSecondLayer)&(S1S2_sum<self.TSumHighSecondLayer))   
            
            F_pos =  self.ScaleFactorFirstLayer*(F1Sig[F1Sig_ind[F1Sig_ind_ind]] - F2Sig[F2Sig_ind[F2Sig_ind_ind]])
            S_pos =  self.ScaleFactorSecondLayer*(S1Sig[S1Sig_ind[S1Sig_ind_ind]] - S2Sig[S2Sig_ind[S2Sig_ind_ind]])
            
            Radius = np.sqrt((F_pos**2)[:,np.newaxis] + (S_pos**2)[np.newaxis,:])
            
            #Mcp radius condition
            FSig_ind_ind_ind, SSig_ind_ind_ind = np.where(Radius<self.McpRadius)      
            
           # Hits = zip(np.ones(len(FSig_ind_ind),dtype=np.float64)*McpT,F1Sig[F1Sig_ind[F1Sig_ind_ind[FSig_ind_ind_ind]]], F2Sig[F2Sig_ind[F2Sig_ind_ind       [FSig_ind_ind_ind]]], S1Sig[S1Sig_ind[S1Sig_ind_ind[SSig_ind_ind_ind]]], S2Sig[S2Sig_ind[S2Sig_ind_ind[SSig_ind_ind_ind]]])
            
  
  #          F1Sig_used_counter[F1Sig_ind[F1Sig_ind_ind[FSig_ind_ind_ind]]] += 1
  #          F2Sig_used_counter[F2Sig_ind[F2Sig_ind_ind[FSig_ind_ind_ind]]] += 1
  #          S1Sig_used_counter[S1Sig_ind[S1Sig_ind_ind[SSig_ind_ind_ind]]] += 1
  #          S2Sig_used_counter[S2Sig_ind[S2Sig_ind_ind[SSig_ind_ind_ind]]] += 1    
            
            if len(FSig_ind_ind_ind) > 0: 
                        
                TSumMetric = np.abs((F1Sig[F1Sig_ind[F1Sig_ind_ind[FSig_ind_ind_ind]]] + F2Sig[F2Sig_ind[F2Sig_ind_ind[FSig_ind_ind_ind]]] + 
                S1Sig[S1Sig_ind[S1Sig_ind_ind[SSig_ind_ind_ind]]] + S2Sig[S2Sig_ind[S2Sig_ind_ind[SSig_ind_ind_ind]]] - 
            self.TSumAvgFirstLayer - self.TSumAvgSecondLayer - 4*McpT))
            
                best_ind = np.argmin(TSumMetric)
                        
                Hits.append([McpT, F_pos[FSig_ind_ind_ind[best_ind]], S_pos[SSig_ind_ind_ind[best_ind]], F1Sig[F1Sig_ind[F1Sig_ind_ind[FSig_ind_ind_ind[best_ind]]]], 
            F2Sig[F2Sig_ind[F2Sig_ind_ind[FSig_ind_ind_ind[best_ind]]]], S1Sig[S1Sig_ind[S1Sig_ind_ind[SSig_ind_ind_ind[best_ind]]]], 
            S2Sig[S2Sig_ind[S2Sig_ind_ind[SSig_ind_ind_ind[best_ind]]]]])
            

            
        return Hits
