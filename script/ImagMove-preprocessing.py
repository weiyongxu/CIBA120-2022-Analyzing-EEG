# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 12:59:40 2022

@author: Weiyong Xu (weiyong.w.xu@jyu.fi)
"""

import mne
from mne.preprocessing import ICA
easycap_montage = mne.channels.make_standard_montage('easycap-M1')

Ids=[9,10,12,13,14,15,16,26,27,28,29,30,31,32,33,34]
data_folder='Z:/psy-interbrain/Shared/Jan/CIBA120_data/raw/'

state='imag'
for id in Ids:
    evoked=dict()
    
    input_fname=data_folder+'ciba%03d_%s.vhdr'%(id,state)
    raw=mne.io.read_raw_brainvision(vhdr_fname=input_fname,preload=True)
    raw.set_montage(easycap_montage)
    raw.plot(n_channels=32,block=True,scalings=dict(eeg=80e-6))
    eeg=raw.filter(None,20).set_eeg_reference('average')
    
    ica = ICA(method='fastica')    
    ica.fit(eeg.copy().filter(1,None),reject = dict(eeg=300e-6),decim=5)
    ica.plot_sources(eeg,block = True) 
    print('reject ICA component: %s'%(ica.exclude))
    ica.apply(eeg,exclude=ica.exclude)    
        
    events=mne.events_from_annotations(eeg)[0]    
    event_id = {'imagine right': 4, 'imagine left': 8, 'rest': 16}
    epochs=mne.Epochs(eeg, events=events, event_id=event_id, tmin=-4, tmax=12)
    epochs.save('imagmove_%03d-epo.fif'%(id),overwrite=True)

 
