#%%
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px
import plotly.figure_factory as ff


#%%
with open('ratings.csv', 'r', encoding='mac_roman', newline='') as csvfile:
    df = pd.read_csv(csvfile)

df = df[df['Title Type'] == 'movie'].copy()
df['Release Date'] = pd.to_datetime(df['Release Date'])
df['Date Rated'] = pd.to_datetime(df['Date Rated'])
df['Diff in ratings'] = round(df['IMDb Rating'] - df['Your Rating'],1)
df['Link'] = '<a href=”' + df['URL'].astype(str) +'”>'+ df['Title'].astype(str) 


df.drop('Title Type', axis=1, inplace=True)
df.to_csv('ratings_clean.csv', index=False)

# Figure out genre stuff
one_hot = df['Genres'].str.get_dummies(sep=', ')

#%%
# Table1
# Make links work
# Make Table narrower and taller
my_ratings = pd.DataFrame()
my_ratings['My Rating'] = [i for i in range(10,0,-1)]
my_ratings['Criteria'] = ['Perfect','Great','Really good','Good','Okay','Average','Not good','Really not good','Bad','Is this even a movie?']
my_ratings['Link'] = ['<a href=”https://www.imdb.com/title/tt0468569/”>The Dark Knight</a>',
        '<a href=”https://www.imdb.com/title/tt0361748/”>Inglourious Basterds</a>',
        '<a href=”https://www.imdb.com/title/tt0993846/”>The Wolf of Wall Street</a>',
        '<a href=”https://www.imdb.com/title/tt1677720/”>Ready Player One</a>',
        '<a href=”https://www.imdb.com/title/tt1219289/”>Limitless</a>',
        '<a href=”https://www.imdb.com/title/tt2461150/”>Masterminds</a>',
        '',
        '<a href=”https://www.imdb.com/title/tt0360556/”>Fahrenheit 451</a>',
        '',
        '<a href=”https://www.imdb.com/title/tt0368226/”>The Room</a>'
]
my_ratings['Title'] = ['The Dark Knight',
'Inglourious Basterds',
'The Wolf of Wall Street',
'Ready Player One',
'Limitless',
'Masterminds',
'',
'Fahrenheit 451',
'',
'The Room'
]


fig = go.Figure(data=[go.Table(
    header=dict(values=['My Rating', 'Criteria', 'Example'],
                align='left'),
    cells=dict(values=[my_ratings['My Rating'], my_ratings['Criteria'], my_ratings['Title']],
               align='left'))])

fig.show()

#%%
# my rating vs. imdb rating
# Scatter1
fig = go.Figure(data=go.Scatter(x=df['Your Rating'],
                                y=df['IMDb Rating'],
                                mode='markers',
                                marker_color=df['Year'],
                                marker=dict(
                                    size=8,
                                    colorscale='Viridis', # one of plotly colorscales
                                    showscale=True),
                                text=df['Title'].astype(str) + ' (' +df['Year'].astype(str) + ' film)')) # fig, ax = plt.subplots(facecolor='#E4E4E4')
fig.show()


#%%
df_diff = df.sort_values(axis=0,by='Diff in ratings').reset_index(drop=True).copy()

# Change to 
# colors = n_colors('#DFAEE6', '#5A2D81', len(df_diff), colortype='hex')

# Table2
# Make taller
# Color just diff in ratings column
# Sort on other columns
fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>Title</b>', '<b>IMDb Rating</b>', '<b>My Rating</b>', '<b>Difference in Ratings</b>'],
    align='center',font=dict(color='black', size=12)
  ),
  cells=dict(
    values=[df_diff['Link'], df_diff['IMDb Rating'], df_diff['Your Rating'], round(df_diff['Diff in ratings'],1)],
    align='left', font=dict(color='black', size=11)
    # ,
    # fill_color=()
    ))
])
plotly.offline.plot(fig, filename='basic-pie-chart')

fig.show()

#%%
# year vs diff in ratings
# Scatter2

#%%
# bar1
# num movies per year
fig, ax = plt.subplots(facecolor='#E4E4E4')
fig.patch.set_facecolor('#E4E4E4')
ax.patch.set_facecolor('#E4E4E4')
plot = ax.bar(df['Year'].value_counts(sort=False).index,df['Year'].value_counts(sort=False).values)
plt.xlabel("Year")
plt.ylabel('# of movies rated')
for i in range(0, len(plot), 2):
    plot[i].set_facecolor('#DFAEE6')
    try:
        plot[i+1].set_facecolor('#5A2D81')
    except:
        continue

plt.title('Number of movies in my ratings by Year Released')
fig.set_size_inches(12,8, forward=True)

#%%
# Table3
# top 5 genres by decade

genres = list(one_hot.sum().sort_values()[(one_hot.sum().sort_values() / len(df)) > .15].index)
one_hot = one_hot[genres].astype(bool).copy()
df = df.join(one_hot)
df = df.drop(['Genres', 'Date Rated'], axis=1)

#%%
df['Decade'] = pd.cut(df['Year'], bins=list(range(1979, 2039, 10)), labels=[str(i+1)[2:] + "'s" for i in range(1979, 2029, 10)], include_lowest=True)
df['IMDb Rating binned'] = df['IMDb Rating'].astype(int)
# Focus on thriller, action, comedy, crime, sci fi
df.drop(['Drama','Biography','Mystery','Adventure'],axis=1,inplace=True)


#%%
# plotly box/whisker1
# x is decade y is my rating

#%%
# plotly box/whisker2
# x is genre y is my rating

#%%
# Change to plt bar
df.groupby('Decade').sum()[['Sci-Fi', 'Crime', 'Comedy', 'Action', 'Thriller']].plot(kind='bar')
# eh idk



# %%
