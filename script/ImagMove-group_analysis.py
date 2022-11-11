# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:08:45 2022

@author: Weiyong Xu (weiyong.w.xu@jyu.fi)
"""
import mne
import numpy as np
from mne.time_frequency import tfr_multitaper

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 

processed_data_folder='C:/Users/subtl/OneDrive/Area/Teaching/CIBA120-2022/CIBA120-2022-Analyzing EEG/processed_data/'

Ids=[9,10,12,13,14,15,16,26,27,28,29,30,31,32,33,34]
freqs = np.arange(8, 16, 1)
baseline=(-2, 0)
state='imag'
conditions=['rest','imagine left','imagine right']
channels=['C3','Cz','C4']

tfr_all=dict()
for id in Ids:
    tfrs=dict()
    epochs=mne.read_epochs(processed_data_folder+'imagmove_%03d-less_channels-epo.fif'%(id)).pick_channels(channels)
    tfr = tfr_multitaper(epochs, freqs=freqs, n_cycles=freqs, use_fft=True,return_itc=False, average=False)
    tfr.crop(-2,10).apply_baseline(baseline, mode="percent")
    for condition in conditions:
           tfrs[condition]=tfr[condition].average()
    tfr_all[id]=tfrs
    
GA_tfr=dict()
for cond in conditions:
    GA_tfr[cond]=mne.grand_average([sub[cond] for sub in tfr_all.values()])
    GA_tfr[cond].comment=cond

GA_tfr['imagine right'].plot_topo(cmap="RdBu")    
GA_tfr['imagine left'].plot_topo(cmap="RdBu")       
GA_tfr['rest'].plot_topo(cmap="RdBu") 

fig, axs = plt.subplots(3, 3,sharex=True, sharey=True)
for i,condition in enumerate(conditions):   
    for j,channel in enumerate(channels):
        GA_tfr[condition].plot([channel],vmin=-0.5, vmax=1,axes=axs[i,j])
        axs[i,j].set_title(condition+'_'+channel)
    

df_list=list()
for id in Ids:
    for condition in conditions:
        df=tfr_all[id][condition].to_data_frame(time_format=None, long_format=True)
        df['condition']=condition
        df['id']=id
        df=df.rename(columns={'value':'ERDS'})
        df_list.append(df)        
df_all=pd.concat(df_list)    


df_all_freq_avg=df_all.groupby(['time','channel','id','condition'])['ERDS'].mean().reset_index()
df_all_freq_avg['channel'] = df_all_freq_avg['channel'].cat.reorder_categories(('C3', 'Cz', 'C4'), ordered=True)

g = sns.FacetGrid(df_all_freq_avg, row=None, col='condition')
g.map(sns.lineplot, 'time', 'ERDS', 'channel', n_boot=10)
axline_kw = dict(color='black', linestyle='dashed', linewidth=0.5, alpha=0.5)
g.map(plt.axhline, y=0, **axline_kw)
g.map(plt.axvline, x=0, **axline_kw)
g.set(ylim=(None, 1.5))
g.set_axis_labels("Time (s)", "ERDS (%)")
g.set_titles(col_template="{col_name}", row_template="{row_name}")
g.add_legend()


g = sns.FacetGrid(df_all, col="id", col_wrap=4, height=2, )
g.map(sns.pointplot, "channel", "ERDS",'condition',palette=sns.color_palette("pastel"))
g.map(plt.axhline, y=0, **axline_kw)
g.set_axis_labels("Channels (s)", "ERDS (%)")
g.add_legend()




df_TW=df_all.query("time > 0.0 & time < 5.0 & condition !='rest' ")
df_TW=df_TW.groupby(['channel','id','condition'])['ERDS'].mean().reset_index()
df_TW['channel'] = df_TW['channel'].cat.reorder_categories(('C3', 'Cz', 'C4'), ordered=True)
df_TW=df_TW[df_TW['channel']!='Cz']
df_TW['channel'].cat.remove_unused_categories(inplace=True)

plt.figure()
sns.boxplot(x="condition", y="ERDS", hue="channel", data=df_TW, palette="Set3")


df_TW.to_csv('ImagMove.csv')
 

import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.graphics.factorplots import interaction_plot
import matplotlib.pyplot as plt
fig = interaction_plot(x=df_TW['condition'], trace=df_TW['channel'], response=df_TW['ERDS'])
plt.show()

#perform two-way ANOVA
model = ols('ERDS ~ C(channel) + C(condition) + C(channel):C(condition)', data=df_TW).fit()
sm.stats.anova_lm(model, typ=2)