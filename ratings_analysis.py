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

color_list = ['#1A4D94', '#007A33', '#CB4F0A', '#5A2D81'] * int(len(df)/3)
full_color_list = ['#1A4D94', '#5C7DAA', '#007A33', '#33955C', '#CB4F0A', '#F58426','#5A2D81', '#DFAEE6'] * int(len(df)/7)

#%%
# Table1
# See if links work when exporting as picture and .html file
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
                fill_color='#5C7DAA',
                font_color='white',
                align='left'),
    cells=dict(values=[my_ratings['My Rating'], my_ratings['Criteria'], my_ratings['Title']],
                fill_color='#E4E4E4',
                font_color='black',
                align='left'))])

fig.show()

#%%
# Scatter1
# my rating vs. imdb rating
# Figure out color scale
fig = go.Figure(data=go.Scatter(x=df['IMDb Rating'],
                                y=df['Your Rating'],
                                mode='markers',
                                marker=dict(
                                    size=8,
                                    color='#007A33'
                                ),
                                hovertemplate=df['Title'].astype(str)+' (' +df['Year'].astype(str) + ' film)'+
                                '<br><b>IMDb Rating</b>: %{x}<br>'+
                                '<b>My Rating</b>: %{y}'+'<extra></extra>'
                                ))
fig.update_layout(
    plot_bgcolor='#e4e4e4',
    title=dict(
        text='IMDb Rating vs. My Rating',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='IMDb Rating'
    ),
    yaxis=dict(
        title='My Rating'
    )
)
fig.show()


#%%
# Table2
# Sort on columns?
# Links?
# Muted color scale
df_diff = df.sort_values(axis=0,by='Diff in ratings').reset_index(drop=True).copy()

colors = n_colors('rgb(24,200,10)','rgb(200,10,24)', len(df_diff), colortype='rgb')
fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>Title</b>', '<b>IMDb Rating</b>', '<b>My Rating</b>', '<b>Difference in Ratings</b>'],
    align='center',font=dict(color='black', size=12)
  ),
  cells=dict(
    values=[df_diff['Link'], df_diff['IMDb Rating'], df_diff['Your Rating'], round(df_diff['Diff in ratings'],1)],
    align='left', font=dict(color=['black', 'black', 'black', 'white'], size=11),
    fill_color=['rgb(228,228,228)','rgb(228,228,228)','rgb(228,228,228)',colors]
    # ,
    # fill_color=()
    ))
])
# plotly.offline.plot(fig, filename='table2')

fig.show()

#%%
# Scatter2
# year vs diff in ratings
# Add text labels
# Add color gradient
fig = go.Figure(data=go.Scatter(x=df['Year'],
                    y=df['Diff in ratings'],
                    mode='markers',
                    # marker_color=df['Runtime (mins)'],
                    marker=dict(
                        size=8,
                        color='#1A4D94'
                    ),
                    hovertemplate=df['Title'].astype(str)+' (' +df['Year'].astype(str) + ' film)'+
                    '<br><b>IMDb Rating</b>: '+df['IMDb Rating'].astype(str)+'<br>'+
                    '<b>My Rating</b>: '+df['Your Rating'].astype(str)+'<br>'+
                    '<b>Difference</b>: %{y}'+'<extra></extra>'
                ))
fig.update_layout(
    plot_bgcolor='#e4e4e4',
    title=dict(
        text='Year vs. Difference in Ratings',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Year'
    ),
    yaxis=dict(
        title='Difference in Ratings'
    )
)
fig.show()

#%%
# bar1
# num movies per year
bar = df.groupby('Year').count()['Title'].copy()
fig = go.Figure(data=go.Bar(x=bar.index,
                    y=bar.values,
                    marker_color=full_color_list[0:len(bar)]
                ))
fig.update_layout(
    plot_bgcolor='#e4e4e4',
    title=dict(
        text='Number of movies in my ratings by year released',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Year'
    ),
    yaxis=dict(
        title='Number of movies rated'
    )
)
fig.show()

#%%
# Table3
# top 5 genres by decade

genres = list(one_hot.sum().sort_values()[(one_hot.sum().sort_values() / len(df)) > .15].index)
one_hot = one_hot[genres].astype(bool).copy()
df = df.join(one_hot)
df = df.drop(['Genres', 'Date Rated'], axis=1)

#%%
df['IMDb Rating binned'] = df['IMDb Rating'].astype(int)
# Focus on thriller, action, comedy, crime, sci fi
df.drop(['Drama','Biography','Mystery','Adventure'],axis=1,inplace=True)


#%%
# plotly box/whisker1
# x is decade y is my rating
# See if I can change colors of decades
df['Decade'] = pd.cut(df['Year'], bins=list(range(1979, 2039, 10)), labels=[str(i+1)[2:] + "'s" for i in range(1979, 2029, 10)], include_lowest=True)

df.sort_values('Year', inplace=True)
fig = go.Figure(data=go.Box(x=df['Decade'],
                    y=df['Your Rating'],
                    marker=dict( 
                        color='#000000'
                    ),
                    line=dict(color='#CB4F0A')
                ))
fig.update_layout(
    plot_bgcolor='#e4e4e4',
    title=dict(
        text='My ratings by decade',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Decade'
    ),
    yaxis=dict(
        title='Rating'
    )
)
fig.show()

#%%
# plotly box/whisker2
# x is genre y is my rating

#%%
# Change to plt bar
df.groupby('Decade').sum()[['Sci-Fi', 'Crime', 'Comedy', 'Action', 'Thriller']].plot(kind='bar')
# eh idk



# %%
