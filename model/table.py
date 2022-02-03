import pandas as pd

df = pd.read_csv('dataset/collaborative_filtering/steam-200k.csv')
df.columns = ['user', 'game', 'action', 'hours','rating']

#df = df[df['action'] == 'play'].copy()



userbyitem = pd.DataFrame(index=df['user'].unique(), columns=df['game'].unique())

for i in range(len(df)):
    user = df.iloc[i]['user']
    game = df.iloc[i]['game']
    userbyitem.loc[user,game] = df.iloc[i]['rating']

#oynama saatleri bir matrix şeklinde bir csv dosyasına aktarıldı
#userbyitem.to_csv('dataset/collaborative_filtering/newDataset/userbyitem.csv', index=True)



print(userbyitem)