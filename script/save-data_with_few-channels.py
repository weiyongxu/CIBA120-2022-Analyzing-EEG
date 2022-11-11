# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 16:09:36 2022

@author: Weiyong Xu (weiyong.w.xu@jyu.fi)
"""

import mne
processed_data_folder='C:/Users/subtl/OneDrive/Area/Teaching/CIBA120-2022/CIBA120-2022-Analyzing EEG/processed_data/'


#oddball
Ids=[9,11,12,13,14,15,26,27,28,29,30,31,32,33,34]
states=['attend','ignore']
evoked_all=dict()
for id in Ids:
    evoked=dict()
    for state in states: 
        epochs=mne.read_epochs(processed_data_folder+'ciba%03d_ob_%s-epo.fif'%(id,state)).pick_channels(['Cz']) 
        epochs.save('ciba%03d_ob_%s-less_channels-epo.fif'%(id,state),overwrite=True)
        

#imagmove
Ids=[9,10,12,13,14,15,16,26,27,28,29,30,31,32,33,34]
state='imag'
for id in Ids:
    epochs=mne.read_epochs(processed_data_folder+'imagmove_%03d-epo.fif'%(id)).pick_channels(['C3','Cz','C4']) 
    epochs.save('imagmove_%03d-less_channels-epo.fif'%(id),overwrite=True)