import pandas as pd
import math
rating = pd.read_csv('dataset/collaborative_filtering/newDataset/playerDataset.csv', usecols=['user', 'game', 'rating'])

user = [
            {'game':'The Elder Scrolls V Skyrim', 'rating':5.0},
            {'game':'Doom 2', 'rating':5.0},
            {'game':'Fallout 4', 'rating':5.0},
         ]


inputGames = pd.DataFrame(user)

#oynanan oyunları, oynayan oyuncuları getirdik
users = rating[rating['game'].isin(inputGames['game'].tolist())]

print(users.shape) #kaç satır ve sütun var

userSubsetGroup = users.groupby(['user']) # kullanıcıları idlerine göre listeledik

#print(userSubsetGroup.get_group(250006052)) # idli kullancıyı getirmek için kullandık

userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)

userSubsetGroup = userSubsetGroup[0:100]

#print(userSubsetGroup)

#Store the Pearson Correlation in a dictionary, where the key is the user Id and the value is the coefficient
pearsonCorDict = {}

# For every user group in our subset
for name, group in userSubsetGroup:
    # Let's start by sorting the input and current user group so the values aren't mixed up later on
    group = group.sort_values(by='game')
    inputGames = inputGames.sort_values(by='game')
    # Get the N for the formula
    n = len(group)
    # Get the review scores for the movies that they both have in common
    temp = inputGames[inputGames['game'].isin(group['game'].tolist())]
    # And then store them in a temporary buffer variable in a list format to facilitate future calculations
    tempRatingList = temp['rating'].tolist()
    # put the current user group reviews in a list format
    tempGroupList = group['rating'].tolist()
    # Now let's calculate the pearson correlation between two users, so called, x and y
    Sxx = sum([i ** 2 for i in tempRatingList]) - pow(sum(tempRatingList), 2) / float(n)
    Syy = sum([i ** 2 for i in tempGroupList]) - pow(sum(tempGroupList), 2) / float(n)
    Sxy = sum(i * j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList) * sum(tempGroupList) / float(
        n)

    # If the denominator is different than zero, then divide, else, 0 correlation.
    if Sxx != 0 and Syy != 0:
        pearsonCorDict[name] = Sxy / math.sqrt(Sxx * Syy)
    else:
        pearsonCorDict[name] = 0


#print(pearsonCorDict.items())



pearsonDF = pd.DataFrame.from_dict(pearsonCorDict, orient='index')
pearsonDF.columns = ['similarityIndex']
pearsonDF['user'] = pearsonDF.index
pearsonDF.index = range(len(pearsonDF))
#print(pearsonDF.head())


topUsers=pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:50]
#print(topUsers.head())

topUsersRating=topUsers.merge(rating, left_on='user', right_on='user', how='inner')
#print(topUsersRating.head())


#Multiplies the similarity by the user's ratings
topUsersRating['weightedRating'] = topUsersRating['similarityIndex']*topUsersRating['rating']
#print(topUsersRating.head())

tempTopUsersRating = topUsersRating.groupby('game').sum()[['similarityIndex','weightedRating']]
tempTopUsersRating.columns = ['sum_similarityIndex','sum_weightedRating']
#print(tempTopUsersRating.head())

#Creates an empty dataframe
recommendation_df = pd.DataFrame()
#Now we take the weighted average
recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating']/tempTopUsersRating['sum_similarityIndex']
recommendation_df['game'] = tempTopUsersRating.index
#print(recommendation_df.head())



recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)
#print(recommendation_df.head(10))


durmus =rating.loc[rating['game'].isin(recommendation_df.head(10)['game'].tolist())]



print(durmus)

#print(user[0]['rating']) #rating alma