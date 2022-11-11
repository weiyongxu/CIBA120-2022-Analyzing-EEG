# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 14:29:46 2022

@author: Weiyong Xu (weiyong.w.xu@jyu.fi)
"""
import mne
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

Ids=[9,11,12,13,14,15,26,27,28,29,30,31,32,33,34]
states=['attend','ignore']

processed_data_folder='C:/Users/subtl/OneDrive/Area/Teaching/CIBA120-2022/CIBA120-2022-Analyzing EEG/processed_data/'

evoked_all=dict()
for id in Ids:
    evoked=dict()
    for state in states: 
        epochs=mne.read_epochs(processed_data_folder+'ciba%03d_ob_%s-less_channels-epo.fif'%(id,state))        
        for condition in epochs.event_id.keys():
            evoked[condition]=epochs[condition].average()
            
        evoked_all[id]=evoked
         
GA_evk=dict()
for cond in evoked.keys():
    GA_evk[cond]=mne.grand_average([sub[cond] for sub in evoked_all.values()])
    GA_evk[cond].comment=cond
mne.viz.plot_compare_evokeds(GA_evk,picks=['Cz'])
diff_attend=mne.combine_evoked([GA_evk['attend/deviant'],GA_evk['attend/standard'],], weights=[1,-1])
diff_ignore=mne.combine_evoked([GA_evk['ignore/deviant'],GA_evk['ignore/standard'],], weights=[1,-1])

mne.viz.plot_compare_evokeds([GA_evk['attend/standard'],GA_evk['attend/deviant'],diff_attend],picks=['Cz'],linestyles=['solid','solid','dotted'])
mne.viz.plot_compare_evokeds([GA_evk['ignore/standard'],GA_evk['ignore/deviant'],diff_ignore],picks=['Cz'],linestyles=['solid','solid','dotted'])        
mne.viz.plot_compare_evokeds([diff_attend,diff_ignore],picks=['Cz'],linestyles=['solid','solid'])        

P3_list=list()
ROI_chs=['Cz']
P3_TW=[0.24,0.28]
for id in Ids:
    P3=dict()
    attend_P3_diff=mne.combine_evoked([evoked_all[id]['attend/deviant'],evoked_all[id]['attend/standard'],], weights=[1,-1])
    ignore_P3_diff=mne.combine_evoked([evoked_all[id]['ignore/deviant'],evoked_all[id]['ignore/standard'],], weights=[1,-1])    
    P3['id']=id
    P3['attend_P3']=attend_P3_diff.crop(P3_TW[0],P3_TW[1]).pick_channels(ROI_chs).to_data_frame(index=None)[ROI_chs].mean().tolist()[0]
    P3['ignore_P3']=ignore_P3_diff.crop(P3_TW[0],P3_TW[1]).pick_channels(ROI_chs).to_data_frame(index=None)[ROI_chs].mean().tolist()[0]
    P3_list.append(P3)

df=pd.DataFrame(P3_list)
plt.figure()       
sns.barplot(df[['attend_P3','ignore_P3']])
sns.swarmplot(df[['attend_P3','ignore_P3']],color='black')
df.to_csv('P3.csv')
print(stats.ttest_rel(df['attend_P3'], df['ignore_P3']))


