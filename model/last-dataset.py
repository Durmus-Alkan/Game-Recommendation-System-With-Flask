import pandas as pd

df = pd.read_csv('dataset/collaborative_filtering/newDataset/rating.csv', usecols=['user', 'game', 'rating'])
df.columns = ['user', 'game', 'rating']

df.to_csv('dataset/collaborative_filtering/newDataset/playerDataset.csv', index=True)

print(df)