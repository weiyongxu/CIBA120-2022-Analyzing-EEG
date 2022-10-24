# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:57:55 2022

@author: wexu
"""

import mne
from mne.preprocessing import ICA
import numpy as np
easycap_montage = mne.channels.make_standard_montage('easycap-M1')
    

Ids=range(26,34)
states=['attend','ignore']

for id in Ids:
    for state in states:
        input_fname='Z:/psy-interbrain/Shared/Jan/CIBA120_data/raw/ciba%03d_ob_%s.vhdr'%(id,state)
        raw=mne.io.read_raw_brainvision(vhdr_fname=input_fname,preload=True)
        raw.set_montage(easycap_montage)
        raw.plot(n_channels=32,block=True,scalings=dict(eeg=80e-6))
        eeg=raw.filter(None,20).set_eeg_reference('average')
        #ICA
        ica = ICA(method='fastica')    
        ica.fit(eeg.copy().filter(1,None),reject = dict(eeg=300e-6),decim=5)
        ica.plot_sources(eeg,block = True) 
        print('reject ICA component: %s'%(ica.exclude))
        ica.apply(eeg,exclude=ica.exclude)    
        #events
        events=mne.events_from_annotations(eeg)[0]
        if np.count_nonzero(events[:,2] == 1) > np.count_nonzero(events[:,2] == 2):
            event_id = {'%s/standard'%(state): 1, '%s/deviant'%(state): 2} 
        else:
            event_id = {'%s/standard'%(state): 2, '%s/deviant'%(state): 1}
        standard_events=np.array([events[i-1] for i,e in enumerate(events) if (e[2]==event_id['%s/deviant'%(state)] and i>0)])
        deviant_events=events[events[:,2]==event_id['%s/deviant'%(state)]]
        #epoch    
        epochs=mne.Epochs(eeg, events=np.concatenate([standard_events,deviant_events]), event_id=event_id, tmin=-0.1, tmax=0.45,reject=dict(eeg=100e-6),baseline=(None,0))
        epochs.equalize_event_counts(event_ids=event_id)
        epochs.save('oddball_%03d-epo.fif'%(id))
        
       
