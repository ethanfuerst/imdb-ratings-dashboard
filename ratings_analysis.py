#%%
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

#%%
with open('ratings.csv', 'r', encoding='mac_roman', newline='') as csvfile:
    df = pd.read_csv(csvfile)

def media_kind(x):
    if x == 'movie':
        return 'Movie'
    elif x == 'tvSeries':
        return 'TV'

df['Release Date'] = pd.to_datetime(df['Release Date'])
df['Date Rated'] = pd.to_datetime(df['Date Rated'])
# Get number of days
df['Days waited to see'] = df['Date Rated'] - df['Release Date']
df['Days waited to see'] = (df['Days waited to see'].astype(int) / int(float('8.64e+13'))).astype(int)
df['Diff in ratings'] = df['IMDb Rating'] - df['Your Rating']

df['Title Type'] = df['Title Type'].apply(media_kind)
df.to_csv('ratings_clean.csv', index=False)
#%%
# Before adding to df, need to remove one-hot columns with very few values
one_hot = df['Genres'].str.get_dummies(sep=', ')

def get_frac(col):
    if len(col.value_counts()) != 2:
        return False
    return col.value_counts()[1] / (col.value_counts()[0]+col.value_counts()[1])

# See if the one-hot columns represent at least 20 percent of the columns
def thres_check(col, thres=.2):
    return get_frac(col) > thres

to_drop = []
for i in one_hot.columns:
    if not thres_check(one_hot[i]):
        to_drop.append(i)
one_hot.drop(to_drop, axis=1, inplace=True)

# Figure out a way to check other values count to drop
# thres = .2
# col = df['Title Type']
# vals = list(col.value_counts().index)
# counts = list(col.value_counts().values)
# for i in range(len(counts)):
#     print(vals[i], counts[i] / sum(counts))
#     if (counts[i] / sum(counts)) < thres:
#         print(col.values[i])

df = pd.concat([df, one_hot], axis=1, sort=False)

# Bin IMDb rating, year, Num Votes, Days waited to see, Diff in ratings


# %%
plt.scatter(df['IMDb Rating'], df['Your Rating'])
plt.title('IMDb Rating vs. My Rating')
plt.xlabel('IMDb Rating')
plt.ylabel('My Rating')
plt.show()

# %%
