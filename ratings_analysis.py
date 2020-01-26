#%%
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

#%%
with open('ratings.csv', 'r', encoding='mac_roman', newline='') as csvfile:
    df = pd.read_csv(csvfile)

df['Release Date'] = pd.to_datetime(df['Release Date'])
df['Date Rated'] = pd.to_datetime(df['Date Rated'])
df['Diff in ratings'] = df['IMDb Rating'] - df['Your Rating']
df = df[df['Title Type'] == 'movie'].copy()

df.drop('Title Type', axis=1, inplace=True)
df.to_csv('ratings_clean.csv', index=False)

one_hot = df['Genres'].str.get_dummies(sep=', ')

# Before adding to df, need to remove one-hot columns with very few values
one_hot = df['Genres'].str.get_dummies(sep=', ')

# for markdown
print('## My movie taste by genre')
print('| Genre | Count |\n|:-|:-|')
for i in range(len(one_hot.sum().sort_values().values) - 1):
    print('|', one_hot.sum().sort_values(ascending=False).index[i], '|', one_hot.sum().sort_values(ascending=False).iloc[i], '|')
print('\n')
genres = list(one_hot.sum().sort_values()[(one_hot.sum().sort_values() / len(df)) > .15].index)
one_hot = one_hot[genres].astype(bool).copy()
df = df.join(one_hot)
df = df.drop(['Genres', 'Date Rated'], axis=1)


df_diff = df.sort_values(axis=0,by='Diff in ratings').reset_index(drop=True).copy()
print('## Top 15 Movies I liked more than IMDb')
print('| Movie Title | IMDb Rating | My Rating | Difference |\n|:-|-|-|-|')
for i in range(15):
    print('|','[' + df['Title'].iloc[i] + ' (' + df['Year'].iloc[i].astype(str) + ')](' + df['URL'].iloc[i] + ')', '|',df_diff['IMDb Rating'].iloc[i], '|', df_diff['Your Rating'].iloc[i], '|', round(df_diff['Diff in ratings'].iloc[i],2),'|')
print('\n')
print('## Top 15 Movies IMDb liked more than me')
print('| Movie Title | IMDb Rating | My Rating | Difference |\n|:-|-|-|-|')
for i in range(len(df_diff) - 1, len(df_diff) - 16, -1):
    print('|','[' + df['Title'].iloc[i] + ' (' + df['Year'].iloc[i].astype(str) + ')](' + df['URL'].iloc[i] + ')', '|',df_diff['IMDb Rating'].iloc[i], '|', df_diff['Your Rating'].iloc[i], '|', round(df_diff['Diff in ratings'].iloc[i],2),'|')

df['Decade'] = pd.cut(df['Year'], bins=[1979, 1989, 1999, 2009, 2019, 2029], labels=["80's", "90's", "00's", "10's", "20's"], include_lowest=True)
df['IMDb Rating binned'] = df['IMDb Rating'].astype(int)


# %%
plt.scatter(df['IMDb Rating'], df['Your Rating'])
plt.title('IMDb Rating vs. My Rating')
plt.xlabel('IMDb Rating')
plt.ylabel('My Rating')
plt.show()

# %%
