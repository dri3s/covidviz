


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


# In[]


path = r"C:\Users\dries\Downloads\PEP_2018_PEPANNCHG.ST05_with_ann.csv"

pop = pd.read_csv(path, encoding='latin1')

pop = pop.rename(columns={'GC.target-geo-id2':'fips',
                'respop72018':'population'})

pop = pop[['fips','population']]

pop = pop.loc[1:]

pop['population'] = pd.to_numeric(pop['population'])
pop['fips'] = pd.to_numeric(pop.fips)


# In[]


path = r"C:\cygwin64\home\dries\scripts\covid-scripts\covidviz\scripts.txt"
msa = pd.read_fwf(path, skiprows=20, names=['msa_fips','fips','x','county'])


# In[]


msa['fips'] = pd.to_numeric(msa.fips, errors='coerce')


# In[]


msa['msa_fips'] = pd.to_numeric(msa.msa_fips, errors='coerce')


# In[]


msa_cty = msa.loc[msa.fips.notna()]


# In[]


msa.loc[msa.fips.isna() & msa.msa_fips.notna()]


# In[]


covid = covid.merge(pop)

covid['date'] = pd.to_datetime(covid.date)

covid['casepercap'] = covid.cases/covid['population']


# In[]


covid = covid.sort_values(by=['fips','date']).reset_index(drop=True)


# In[]


covid = covid.loc[covid.cases >= 10]


# In[]


covid ['num_days'] = (covid.date - covid.groupby(['fips'])['date'].transform('min')).dt.days


# In[]


biguns = covid.loc[covid.population >= 100e3].fips.unique().tolist()
worst = list(covid.groupby('fips').cases.max().reset_index().sort_values('cases').tail(7).fips.values)
dets_names = ['Harris','Fort Bend','Brazoria','Montgomery','Galveston']
dets = covid.loc[(covid.county.isin(dets_names)) & (covid.state == 'Texas')].fips.unique()
worst  = [d for d in worst if d not in dets]
grays = [f for f in biguns if f not in dets and f not in worst]


# In[]


colors = iter(sns.color_palette('husl', len(dets) + len(worst)))

plt.rcParams['figure.figsize'] = 15, 5
fig, ax = plt.subplots()

for fips in grays + list(worst) + list(dets):
    county = covid.loc[covid.fips == fips].county.unique()[0]
    state = covid.loc[covid.fips == fips].state.unique()[0]    
    
    if fips in worst:
        label = county + ' County, ' + state
        color = next(colors)
        lw, alpha = (1, 1)
    elif fips in dets:
        label = county
        color = next(colors)
        lw, alpha = (5, 1)
    else:
        label = None
        color='gray'
        lw, alpha = (0.4, 0.4)
    
    #ax.plot(covid.loc[covid.fips == fips]['date'],
    ax.plot(covid.loc[covid.fips == fips]['num_days'],
            covid.loc[covid.fips == fips]['casepercap'] * 1e3, 
            label=label,
            color=color,
            lw=lw,
            alpha=alpha
            )

#ax.set_xlim([pd.to_datetime('15feb2020'),pd.to_datetime(date.today())])
#ax.xaxis.set_major_formatter(myFmt)
#ax.xaxis.set_major_locator(mdates.WeekdayLocator(mdates.MO))

ax.set_xlim([0, covid.num_days.max()])
ax.set_yscale('log')

ax.set_ylabel('COVID Cases per 1,000 people')
ax.set_xlabel('Num Days Since 10th Case')
ax.legend()
ax.grid()

#plt.savefig(r'c:\users\dries\graph.png')


# In[]


np.log(8)/np.log(2)


# In[]


