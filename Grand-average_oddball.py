# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 14:29:46 2022

@author: subtl
"""
    

GA=dict()
for id in Ids:
        evoked=dict()
        for condition in event_id.keys():
            evoked[condition]=epochs[condition].average()
        GA[id]=evoked
        #mne.viz.plot_compare_evokeds(evoked,picks=['Cz'])
         
GA_evk=dict()
for cond in evoked.keys():
    GA_evk[cond]=mne.grand_average([sub[cond] for sub in GA.values()])
    GA_evk[cond].comment=cond
mne.viz.plot_compare_evokeds(GA_evk,picks=['Cz'])
diff_attend=mne.combine_evoked([GA_evk['attend/deviant'],GA_evk['attend/standard'],], weights=[1,-1])
diff_ignore=mne.combine_evoked([GA_evk['ignore/deviant'],GA_evk['ignore/standard'],], weights=[1,-1])

mne.viz.plot_compare_evokeds([GA_evk['attend/standard'],GA_evk['attend/deviant'],diff_attend],picks=['Cz'],linestyles=['solid','solid','dotted'])
mne.viz.plot_compare_evokeds([GA_evk['ignore/standard'],GA_evk['ignore/deviant'],diff_ignore],picks=['Cz'],linestyles=['solid','solid','dotted'])        