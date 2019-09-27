# Adapted from OnDA's parallelization script. I used "MPI Reduce" instead of "SendRecv" as used by OnDA,
#And the change is to improve the processing speed for offline coincidence data analysis.



import sys
import psana
from mpi4py import MPI

import math
import time
import datetime

import numpy as np

import lib.onda.cfelpyutils.cfelpsana as cpsana

from lib.onda.utils import (
    global_params as gp,
    dynamic_import as dyn_imp
)

de_layer = dyn_imp.import_layer_module('data_extraction_layer',
                                       gp.monitor_params)
extract = getattr(de_layer, 'extract')


class Workers(object):

    NOMORE = 998
    DIETAG = 999
    DEADTAG = 1000

    def __init__(self, map_func, reduce_func, save_func, source, monitor_params):

        debug = False

        self.psana_source = None
        self._buffer = None
        self.event_timestamp = None

        self.mpi_rank = MPI.COMM_WORLD.Get_rank()
        self.mpi_size = MPI.COMM_WORLD.Get_size()
        if self.mpi_rank == 0:
            self.role = 'master'
        else:
            self.role = 'worker'

        self.monitor_params = monitor_params
        psana_params = monitor_params['PsanaParallelizationLayer']



        self.offline = False
        self.source = source

        if 'shmem' not in self.source and debug is False:
            self.offline = True
            if not self.source[-4:] == ':idx':
                self.source += ':idx'

        self.map = map_func
        self.reduce = reduce_func
        self.save_func = save_func
        self.extract_data = extract


        
        if self.role == 'worker':
            self.num_lost_events_evt = 0        
            self.num_lost_events_time = 0
            self.num_lost_events_data = 0   
               
            self.num_failed_events = 0               
            self.num_reduced_events = 0
            
        if self.role == 'master':
            self.num_lost_events_evt = 0                    
            self.num_lost_events_time = 0
            self.num_lost_events_data = 0 
            
            self.num_failed_events = 0                           
            self.num_reduced_events = 0
            self.num_nomore = 0


        return


    def start(self, verbose=False):


        req = None


        self.psana_source = psana.DataSource(self.source)

        if self.offline is False:
            psana_events = self.psana_source.events()
        else:
            def psana_events_generator():
                for i_run,r in enumerate(self.psana_source.runs()):
                    print(str(self.mpi_rank)+' process run')
                    print(i_run)
                    MPI.COMM_WORLD.Barrier()
                    times = r.times()
                    inds_for_all = np.arange(len(times))
                    mylength = int(math.ceil(len(times) / float(self.mpi_size)))
                    mytimes = times[(self.mpi_rank) * mylength: (self.mpi_rank+1) * mylength]
                    inds_mine = inds_for_all[(self.mpi_rank) * mylength: (self.mpi_rank+1) * mylength]
                        
                    for i_evt_mine,mt in enumerate(mytimes):
                        yield [i_run,inds_mine[i_evt_mine],r.event(mt)]                        

            i_psana_events = psana_events_generator()

        event = {'monitor_params': self.monitor_params}

        for irun_ievt_evt in i_psana_events:
            try:
                self.irun = irun_ievt_evt[0]
                self.ievt = irun_ievt_evt[1]
                evt = irun_ievt_evt[2]
                if evt is None:
                    self.num_lost_events_evt += 1            
                    continue

                event_id = evt.get(psana.EventId)
                timestring = str(event_id).split('time=')[1].split(',')[0]
                timestamp = time.strptime(timestring[:-6], '%Y-%m-%d %H:%M:%S.%f')
                timestamp = datetime.datetime.fromtimestamp(time.mktime(timestamp))
                timenow = datetime.datetime.now()

         
                event['evt'] = evt

                
                self.extract_data(event, self)

                if self.eImage is None:
                    self.num_lost_events_data += 1
                    continue
                    
                self.map()
                self.num_reduced_events += 1
                
            except Exception as e:
                self.num_failed_events += 0                           
                print('rank '+str(self.mpi_rank)+' failed at event '+str(irun_ievt_evt[1]))
                print(e)

        
        print(str(self.mpi_rank)+' completed sorting.')
        MPI.COMM_WORLD.Barrier()
        self.reduce()     

        if self.role == 'worker':

            end_dict = {'end': True,'num_lost_events_time': self.num_lost_events_time,'num_lost_events_data': self.num_lost_events_data,'num_lost_events_evt': self.num_lost_events_evt,'num_reduced_events': self.num_reduced_events,'num_failed_events': self.num_failed_events}

            MPI.COMM_WORLD.isend((end_dict, self.mpi_rank), dest=0, tag=0)
            MPI.Finalize()
            sys.exit(0)
            
        if self.role == 'master':


            while True:

                try:

                    buffer_data = MPI.COMM_WORLD.recv(
                        source=MPI.ANY_SOURCE,
                        tag=0)
                        
                    if 'end' in buffer_data[0].keys():

                        self.num_lost_events_time += buffer_data[0]['num_lost_events_time']
                        self.num_lost_events_data += buffer_data[0]['num_lost_events_data']  
                        self.num_lost_events_evt += buffer_data[0]['num_lost_events_evt']  
                        self.num_failed_events += buffer_data[0]['num_failed_events']                                           
                        self.num_reduced_events += buffer_data[0]['num_reduced_events']                                            
                                              
                        print ('Finalizing {0}'.format(buffer_data[1]))
                        self.num_nomore += 1
                        if self.num_nomore == self.mpi_size - 1:

                            print('All workers have run out of events.')
                            
                            self.save_func(self.num_lost_events_time,self.num_lost_events_data,
                            self.num_lost_events_evt,self.num_failed_events,self.num_reduced_events)   
                                                                             
                            print('Shutting down.')
                            self.end_processing()

                            MPI.Finalize()
                            sys.exit(0)
                        continue



                except KeyboardInterrupt as e:
                    print ('Recieved keyboard sigterm...')
                    print (str(e))
                    print ('shutting down MPI.')
                    self.shutdown()
                    print ('---> execution finished.')
                    sys.exit(0)   


        return


    def shutdown(self, msg='Reason not provided.'):

        print ('Shutting down: {0}'.format(msg))

        if self.role == 'worker':
            self._buffer = MPI.COMM_WORLD.send(dest=0, tag=self.DEADTAG)
            MPI.Finalize()
            sys.exit(0)

        if self.role == 'master':

            try:
 
                num_shutdown_confirm = 0
                while True:
                    if MPI.COMM_WORLD.Iprobe(source=MPI.ANY_SOURCE, tag=0):
                        self._buffer = MPI.COMM_WORLD.recv(source=MPI.ANY_SOURCE, tag=0)
                    if MPI.COMM_WORLD.Iprobe(source=MPI.ANY_SOURCE, tag=self.DEADTAG):
                        num_shutdown_confirm += 1
                    if num_shutdown_confirm == self.mpi_size() - 1:
                        break
                MPI.Finalize()
            except Exception:
                MPI.COMM_WORLD.Abort(0)
            sys.exit(0)
        return
        
    def end_processing(self):
        print('Processing finished. Processed {0} events in total.'.format(self.num_reduced_events))
        
        pass
