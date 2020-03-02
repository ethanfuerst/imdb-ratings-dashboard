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

#%%
# for markdown
print('## My movie taste by genre')
print('')
print('| Genre | Count |\n|:-|:-|')
for i in range(len(one_hot.sum().sort_values().values) - 1):
    print('|', one_hot.sum().sort_values(ascending=False).index[i], '|', one_hot.sum().sort_values(ascending=False).iloc[i], '|')
print('\n')
genres = list(one_hot.sum().sort_values()[(one_hot.sum().sort_values() / len(df)) > .15].index)
one_hot = one_hot[genres].astype(bool).copy()
df = df.join(one_hot)
df = df.drop(['Genres', 'Date Rated'], axis=1)


df_diff = df.sort_values(axis=0,by='Diff in ratings').reset_index(drop=True).copy()
print('## Top 10 Movies I liked more than IMDb')
print('')
print('| Movie Title | IMDb Rating | My Rating | Difference |\n|:-|-|-|-|')
for i in range(10):
    print('|','[' + df_diff['Title'].iloc[i] + ' (' + df_diff['Year'].iloc[i].astype(str) + ')](' + df_diff['URL'].iloc[i] + ')', '|',df_diff['IMDb Rating'].iloc[i], '|', df_diff['Your Rating'].iloc[i], '|', round(df_diff['Diff in ratings'].iloc[i],2),'|')
print('\n')
no9_10 = df[df['Your Rating'] < 9].sort_values(axis=0,by='Diff in ratings').reset_index(drop=True).copy()
print("## Top 10 Movies I liked more than IMDb (no 9's or 10's)")
print('')
print('| Movie Title | IMDb Rating | My Rating | Difference |\n|:-|-|-|-|')
for i in range(10):
    print('|','[' + no9_10['Title'].iloc[i] + ' (' + no9_10['Year'].iloc[i].astype(str) + ')](' + no9_10['URL'].iloc[i] + ')', '|',no9_10['IMDb Rating'].iloc[i], '|', no9_10['Your Rating'].iloc[i], '|', round(no9_10['Diff in ratings'].iloc[i],2),'|')
print('\n')
lt8 = df[df['Your Rating'] < 8].sort_values(axis=0,by='Diff in ratings').reset_index(drop=True).copy()
print("## Top 10 Movies I liked more than IMDb (no 8's, 9's or 10's)")
print('')
print('| Movie Title | IMDb Rating | My Rating | Difference |\n|:-|-|-|-|')
for i in range(10):
    print('|','[' + lt8['Title'].iloc[i] + ' (' + lt8['Year'].iloc[i].astype(str) + ')](' + lt8['URL'].iloc[i] + ')', '|',lt8['IMDb Rating'].iloc[i], '|', lt8['Your Rating'].iloc[i], '|', round(lt8['Diff in ratings'].iloc[i],2),'|')
print('\n')
print('## Top 15 Movies IMDb liked more than me')
print('')
print('| Movie Title | IMDb Rating | My Rating | Difference |\n|:-|-|-|-|')
for i in range(len(df_diff) - 1, len(df_diff) - 16, -1):
    print('|','[' + df_diff['Title'].iloc[i] + ' (' + df_diff['Year'].iloc[i].astype(str) + ')](' + df_diff['URL'].iloc[i] + ')', '|',df_diff['IMDb Rating'].iloc[i], '|', df_diff['Your Rating'].iloc[i], '|', round(df_diff['Diff in ratings'].iloc[i],2),'|')

#%%
fig, ax = plt.subplots(facecolor='#E4E4E4')
fig.patch.set_facecolor('#E4E4E4')
ax.patch.set_facecolor('#E4E4E4')
m, bins, plot = ax.hist(df['IMDb Rating'], bins=[x/5 for x in range(0,50)])
plt.xlabel("IMDb Rating")
xint = [x/2 for x in range(0,20)]
plt.title('Number of movies in my ratings by IMDb Rating')
plt.xticks(xint)
plt.ylabel('# of movies')
fig.set_size_inches(12,7, forward=True)
for i in range(0, len(plot)-4, 4):
    plot[i].set_facecolor('#1A4D94')
    plot[i+1].set_facecolor('#007A33')
    plot[i+2].set_facecolor('#CB4F0A')
    plot[i+3].set_facecolor('#5A2D81')

#%%
df['Decade'] = pd.cut(df['Year'], bins=list(range(1979, 2039, 10)), labels=[str(i+1)[2:] + "'s" for i in range(1979, 2029, 10)], include_lowest=True)
df['IMDb Rating binned'] = df['IMDb Rating'].astype(int)
# Focus on thriller, action, comedy, crime, sci fi
df.drop(['Drama','Biography','Mystery','Adventure'],axis=1,inplace=True)

# number of records for each decade
plt.bar(df['Decade'].value_counts(sort=False).index,df['Decade'].value_counts(sort=False).values)



# box and whisker plot for my rating - one with genre and one with decade on x axis

# %%
# top 5 genres by decade

# %%
# Is there correlation?
plt.scatter(df['IMDb Rating'], df['Your Rating'])
plt.title('IMDb Rating vs. My Rating')
plt.xlabel('IMDb Rating')
plt.ylabel('My Rating')
plt.show()

'''
Post that
'''

#%%
# Change to plt bar
df.groupby('Decade').sum()[['Sci-Fi', 'Crime', 'Comedy', 'Action', 'Thriller']].plot(kind='bar')
# eh idk

