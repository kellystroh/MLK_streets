import pandas as pd
import numpy as np
import glob
import re

path = r'/Users/Kelly/galvanize/projects/circles/MLK/midwest/us'
files = glob.glob(path + '/*' + "/*.csv")
states = []
cities = []
for x in files:
    x = re.sub('/Users/Kelly/galvanize/projects/circles/MLK/midwest/us/', '', x)
    x = re.sub('/.*', '', x)
    states.append(x)

for x in files:
    x = re.sub('/Users/Kelly/galvanize/projects/circles/MLK/midwest/us/.*/', '', x)
    x = re.sub('.csv', '', x)
    cities.append(x)

luther_df_MW = pd.DataFrame(columns=['LON', 'LAT', 'NUMBER', 'STREET', 'UNIT', 'CITY', 'DISTRICT', 'REGION',
       'POSTCODE', 'ID', 'HASH'])

for csv in range(len(files)):
    if csv % 50 == 0:
        print(csv)
    x = pd.read_csv(files[csv], dtype={'LON':'float64', 'LAT':'float64', 'NUMBER':'str', 'STREET':'str', 'UNIT':'str', 'CITY':'str', 'DISTRICT':'str', 'REGION':'str',
       'POSTCODE':'str', 'ID':'str', 'HASH':'str'})
    x.drop(['NUMBER', 'UNIT', 'ID', 'HASH'], axis=1)
    if len(x) == len(x[x.CITY.isna()]):
        x['CITY'] = cities[csv]
        print('woo')
    x['REGION'] = states[csv]
    x = x[~x.STREET.isna()]
    x.drop_duplicates(subset='STREET', keep='first', inplace = True)
    x['STREET'] = x.STREET.str.lower()
    new = x[x.STREET.str.contains("luther")]
    new2 = x[x.STREET.str.contains("mlk")]
    luther_df_MW = pd.concat([luther_df_MW, new, new2], axis=0, ignore_index=True)
luther_df_MW.to_csv('luther_df_MW.csv')