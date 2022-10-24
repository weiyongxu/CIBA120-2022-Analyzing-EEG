# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:08:45 2022

@author: subtl
"""
import mne
import numpy as np
from mne.time_frequency import tfr_morlet
freqs = np.arange(8, 16, 1)
n_cycles =10

Ids=range(26,35)
state='imag'
conditions=['imagine right','imagine left','rest']
GA=dict()

for id in Ids:
    tfr=dict()
    epochs=mne.read_epochs('imagmove_%03d-epo.fif'%(id))
    for condition in conditions:
        tfr[condition]=tfr_morlet(epochs[condition], freqs=freqs, n_cycles=n_cycles,n_jobs=8,decim=4,return_itc=False)     
    GA[id]=tfr
    
GA_tfr=dict()
for cond in conditions:
    GA_tfr[cond]=mne.grand_average([sub[cond] for sub in GA.values()])
    GA_tfr[cond].comment=cond

GA_tfr['rest'].plot_topo(baseline=(-2, 0), mode= 'percent')

    
    
# for id in Ids:
#     evoked=dict()
#     epochs=mne.read_epochs('imagmove_%03d-epo.fif'%(id))
#     epochs.load_data()
#     epochs.apply_hilbert(envelope=True)
#     epochs.crop(-2,10).apply_baseline((-2,0))
#     for condition in conditions:
#         evoked[condition]=epochs[condition].average()     
#     GA[id]=evoked