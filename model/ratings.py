import pandas as pd
import re

ds = pd.read_csv('dataset/collaborative_filtering/steam-200k.csv', header=None).drop(4,axis=1)
ds.columns = ['user', 'game', 'action', 'hours']


ds = ds[ds['action'] == 'play'].copy()

for i, row in ds.iterrows():
    if(row['hours'] >= 40):
        ds.at[i, 'rating'] = 5
    elif( row['hours'] >= 30 and row['hours']<40):
        ds.at[i, 'rating'] = 4
    elif (row['hours'] >= 20 and row['hours'] < 30):
        ds.at[i, 'rating'] = 3
    elif (row['hours'] >= 10 and row['hours'] < 20):
        ds.at[i, 'rating'] = 2
    elif (row['hours'] > 0 and row['hours'] < 10):
        ds.at[i, 'rating'] = 1
    else:
        ds.at[i, 'rating'] = 0
for i, row in ds.iterrows():
    clean = re.sub('[^A-Za-z0-9]+', '', str(row["game"])) #Burada str olmasa, aynı object değil hatası alırız
    clean = clean.lower()
    ds.at[i, 'gameid'] = clean
ds.to_csv('dataset/collaborative_filtering/newDataset/rating.csv', index=True)
print(ds)