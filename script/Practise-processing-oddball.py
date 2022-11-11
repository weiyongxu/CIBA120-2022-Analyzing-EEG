# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:47:34 2022

@author: Weiyong Xu (weiyong.w.xu@jyu.fi)
"""

import mne
from mne.preprocessing import ICA
import numpy as np
easycap_montage = mne.channels.make_standard_montage('easycap-M1')
   
#change the following 3 lines!
data_folder='Z:/psy-interbrain/Shared/Jan/CIBA120_data/raw/'  #change to the folder where the raw EEG data is stored
id=9 #two example subjects: 9 and 12
state='attend' # state can be 'attend' or 'ignore'


#define the input file name
input_fname=data_folder+'ciba%03d_ob_%s.vhdr'%(id,state)

#read raw eeg data
raw=mne.io.read_raw_brainvision(vhdr_fname=input_fname,preload=True)

#set eeg montage to easycap
raw.set_montage(easycap_montage)

#plot eeg , mark bad channels here
raw.plot(n_channels=32,block=True,scalings=dict(eeg=80e-6))

#filter and rereference the EEG data
eeg=raw.filter(None,20).set_eeg_reference('average')

#ICA
ica = ICA(method='fastica')    
ica.fit(eeg.copy().filter(1,None),reject = dict(eeg=300e-6),decim=5)

#plot ICA component, mark component to reject here
ica.plot_sources(eeg,block = True) 
print('reject ICA component: %s'%(ica.exclude))
ica.apply(eeg,exclude=ica.exclude)    

#define std and dev events
events=mne.events_from_annotations(eeg)[0]
if np.count_nonzero(events[:,2] == 1) > np.count_nonzero(events[:,2] == 2):
    event_id = {'%s/standard'%(state): 1, '%s/deviant'%(state): 2} 
else:
    event_id = {'%s/standard'%(state): 2, '%s/deviant'%(state): 1}

#only select the std trial before the dev trial 
standard_events=np.array([events[i-1] for i,e in enumerate(events) if (e[2]==event_id['%s/deviant'%(state)] and i>0)])
deviant_events=events[events[:,2]==event_id['%s/deviant'%(state)]]

#make epochs and try to equalize the std and dev conditions trial counts
epochs=mne.Epochs(eeg, events=np.concatenate([standard_events,deviant_events]), event_id=event_id, tmin=-0.1, tmax=0.45,reject=dict(eeg=100e-6),baseline=(None,0))
epochs.equalize_event_counts(event_ids=event_id)
# save epoch data
epochs.save('ciba%03d_ob_%s-epo.fif'%(id,state),overwrite=True)

#average epochs based on conditions
evoked_list=[epochs[event].average() for event in event_id.keys()]

#plot the evoked topo figure
mne.viz.plot_evoked_topo(evoked_list)        