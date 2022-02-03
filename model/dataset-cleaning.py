import pandas as pd
import re
path = "dataset/content_base/game_dataset.csv"
#dataGames = pd.read_csv(path, usecols=["name", "genre", "game_details", "popular_tags", "publisher", "developer","all_reviews"])
playerGames = pd.read_csv('dataset/collaborative_filtering/Steam_Player.csv')
#Tablonun başlıklarını ekledik
playerGames.columns = ['user', 'game', 'action', 'hours']

#purchase olan kısımlarını sildik
playerGames = playerGames[playerGames['action'] == 'play'].copy()

#id olarak isimlerin harflerini küçültüp, özel karakterleri silerek verdik
for i, row in playerGames.iterrows():
    clean = re.sub('[^A-Za-z0-9]+', '', str(row["game"])) #Burada str olmasa, aynı object değil hatası alırız
    clean = clean.lower()

    playerGames.at[i, 'ID'] = clean




#Yeni bir dataset oluşturup dosyaya kaydettik
playerGames.to_csv('dataset/collaborative_filtering/newDataset/playerGames.csv', index=True)
print(playerGames)