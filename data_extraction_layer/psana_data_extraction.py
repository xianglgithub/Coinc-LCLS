#data extraction script for the coincidence experiment


import psana

import numpy as np

from lib.onda.utils import (
    global_params as gp,
    dynamic_import as dyn_imp
)


def pulse_energy_dataext(event):
    gmd = psana.Detector(str(gp.monitor_params['DetectorLayer']['pulse_eng_detector'])).get(event['evt'])
    if gp.monitor_params['OutputLayer']['pulse_eng_type'] == 63:
     #   print 'pulse eng type 63, 63'
        return gmd.f_63_ENRC()
    if gp.monitor_params['OutputLayer']['pulse_eng_type'] == 64: 
     #   print 'pulse eng type 64, 64'    
        return gmd.f_64_ENRC()    
        
    if gp.monitor_params['OutputLayer']['pulse_eng_type'] == 21:
     #   print 'pulse eng type 21'
        return gmd.f_21_ENRC()
    if gp.monitor_params['OutputLayer']['pulse_eng_type'] == 22: 
     #   print 'pulse eng type 22'    
        return gmd.f_22_ENRC()           
        
    return None

    

def photon_energy_dataext(event):
    return psana.Detector(str(gp.monitor_params['DetectorLayer']['photon_eng_detector'])).get(event['evt']).ebeamPhotonEnergy()
    
def ebeam_energy_dataext(event):

    return psana.Detector(str(gp.monitor_params['DetectorLayer']['photon_eng_detector'])).get(event['evt']).ebeamL3Energy()
    
    
def xlensP_dataext(event):
    
    xlensP_Det = psana.Detector(str(gp.monitor_params['DetectorLayer']['xlensp_detector']))

    return xlensP_Det(event['evt'])    
    
def ylensP_dataext(event):
    ylensP_Det = psana.Detector(str(gp.monitor_params['DetectorLayer']['ylensp_detector']))

    return ylensP_Det(event['evt'])     
         
         
         
def pvcontrol_dataext(event):
    
    pvcontrol_Det = psana.Detector(str(gp.monitor_params['DetectorLayer']['pvcontrolv_detector']))

    return pvcontrol_Det(event['evt']).pvControls()[0].value()       
    
    
def evtcode_dataext(event):
    
    evtcode_Det = psana.Detector(str(gp.monitor_params['DetectorLayer']['evtcode_detector']))

    return evtcode_Det.eventCodes(event['evt'])   

def acqiris_data_dataext(event):
     
    return psana.Detector(str(gp.monitor_params['DetectorLayer']['delayline_detector'])).raw(event['evt'])
    
def acqiris1_data_dataext(event):
    return psana.Detector(str(gp.monitor_params['DetectorLayer']['delayline_detector1'])).raw(event['evt'])    
    
def opal_data_dataext(event):
    rawimg = psana.Detector(str(gp.monitor_params['DetectorLayer']['opal_detector'])).raw(event['evt'])

    return rawimg




def extract1(event, monitor):

    try:
        monitor.acqiris_data_wf, monitor.acqiris_data_wt = acqiris_data_dataext(event)
        monitor.acqiris_data_wt = monitor.acqiris_data_wt*1e9
        

        #monitor.pvctrlV = pvcontrol_dataext(event)    
        
        monitor.pvctrlV = 8.3       
        
        monitor.eImage = 10
        
        monitor.pulse_eng = 10
        monitor.photon_eng = 10
        
        monitor.ebeam_eng = 10
        
        monitor.xlensP = 10
        monitor.ylensP = 10         


    except Exception as e:
        print ('Error when extracting data: {0}'.format(e))
        monitor.acqiris_data_wf = None
        monitor.acqiris_data_wt = None
      
        monitor.pvctrlV = None       
        
def extract(event, monitor):

    try:
        
        monitor.eImage = opal_data_dataext(event)        
        
        monitor.pulse_eng = pulse_energy_dataext(event)
        monitor.photon_eng = photon_energy_dataext(event)   

        monitor.ebeam_eng = ebeam_energy_dataext(event)   
        

        
      
                 
                            

    except Exception as e:
        print ('Error when extracting data: {0}'.format(e))

        monitor.eImage = None
        
        monitor.pulse_eng = None
        
        monitor.ebeam_eng = None
        
def extractE(event, monitor):

    try:

        monitor.eImage_f = opal_data_dataext(event)        
        
        monitor.pulse_eng_f = pulse_energy_dataext(event)
        monitor.photon_eng_f = photon_energy_dataext(event)   
                                   

    except Exception as e:
        print ('Error when extracting data: {0}'.format(e))

        monitor.eImage_f = None
        
        monitor.pulse_eng_f = None
        monitor.photon_eng_f = None        
      
        
                  
        
        
   
                
        

                

   
