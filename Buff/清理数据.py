import csv
import pandas as pd
df = pd.read_csv('arms.csv', encoding='utf-8')
df.drop(columns=['biglabel_link'], inplace=True)
name = df.name.map(lambda x:x.split('|')[-1])
df.name = name
# print(df.head())
# df.to_csv('arms1.csv', index=False, encoding='utf-8')
name1 = df.name.map(lambda x:x.split('(')[0])
df.name = name1
df['name'] = df['name'].str.replace(' ', '')


mask = df['weapon_type'] == 'weapon_knife_kukri'
df.loc[mask, 'weapon_type'] = '廓尔喀刀'

print(df.head())
df.to_csv('arms1.csv', index=False, encoding='utf-8')