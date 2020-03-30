


# In[]


import pandas as pd

from matplotlib import pyplot as plt

import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%a\n%m/%d')

from datetime import date

import seaborn as sns


# In[]


import numpy as np


# In[]


#path = r"C:\cygwin64\home\dries\scripts\covid-19-data\us-counties.csv"
path = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
covid = pd.read_csv(path)
covid['date'] = pd.to_datetime(covid.date)

# In[]


#path = r"C:\Users\dries\Downloads\PEP_2018_PEPANNCHG.ST05_with_ann.csv"
path = 'http://www.wtad.com/assets/news_files/PEP_2018_PEPANNCHG.ST05_with_ann.xlsx'
pop = pd.read_excel(path)


pop = pop.rename(columns={'GC.target-geo-id2':'fips',
                'respop72018':'population'})

pop = pop[['fips','population']]

pop = pop.loc[1:]

pop['population'] = pd.to_numeric(pop['population'])
pop['fips'] = pd.to_numeric(pop.fips)


# In[]

path = "G:\covidviz\metrolist.csv"
msa = pd.read_csv(path, nrows=1160, header=None, names=['msa_fips','msa_name','fips','county_name'])
msa.fips = pd.to_numeric(msa['fips'])
msa = msa.drop(columns=['msa_fips','county_name'])


# In[]


covidmsa = covid.merge(pop).merge(msa)


# In[]

covidmsa = covidmsa.drop(columns='fips').groupby(['date','msa_name']).sum().reset_index()

# In[]



covidmsa['casepercap'] = covidmsa.cases/covidmsa['population']
covidmsa = covidmsa.sort_values(by=['msa_name','date']).reset_index(drop=True)
covidmsa = covidmsa.loc[covidmsa.cases >= 10]


# In[]


covidmsa ['num_days'] = (covidmsa.date - covidmsa.groupby(['msa_name'])['date'].transform('min')).dt.days


# In[]



worst = list(covidmsa.groupby('msa_name').casepercap.max().reset_index().sort_values('casepercap').tail(10).msa_name.values)



# In[]

dets = list(covidmsa.loc[covidmsa.msa_name.str.contains('Dallas')].msa_name.unique())
dets.append(covidmsa.loc[covidmsa.msa_name.str.contains('Houston')].msa_name.unique()[0])

# In[]


colors = iter(sns.color_palette('husl', len(worst) + len(dets)))

plt.rcParams['figure.figsize'] = 15, 5
fig, ax = plt.subplots()

for msaname, df in covidmsa.groupby('msa_name'):          
    df = df.sort_values(by='num_days')
    
    if msaname in worst or msaname in dets:
        label = msaname
        color = next(colors)
        lw, alpha = (3, 1)    
    else:        
        label = '_nolabel_'
        color='gray'
        lw, alpha = (0.4, 0.4)
    
    #ax.plot(covidmsa.loc[covidmsa.fips == fips]['date'],
    ax.plot(df['num_days'],
            df['casepercap'] * 1e3, 
            label=label,
            color=color,
            lw=lw,
            alpha=alpha
            )

#ax.set_xlim([pd.to_datetime('15feb2020'),pd.to_datetime(date.today())])
#ax.xaxis.set_major_formatter(myFmt)
#ax.xaxis.set_major_locator(mdates.WeekdayLocator(mdates.MO))

ax.set_xlim([0, covidmsa.num_days.max()])
ax.set_yscale('log')

ax.set_ylabel('covidmsa Cases per 1,000 people')
ax.set_xlabel('Num Days Since 10th Case')
ax.legend()
ax.grid()




# In[]


np.log(8)/np.log(2)


# In[]


