# %%
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import datetime
import math
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.io as pio
from plotly.colors import n_colors
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import chart_studio
api_key = f = open("plotly_key.txt", "r").readline()
chart_studio.tools.set_credentials_file(username='ethanfuerst', api_key=api_key)

# - Change to see all graphs when run
show_all = False
update_layouts = True

# %%

def imdb_data():
    # - import and clean data
    with open('ratings.csv', 'r', encoding='mac_roman', newline='') as csvfile:
        df = pd.read_csv(csvfile)
    
    # * preliminary data cleaning
    df = df[df['Title Type'] == 'movie'].copy()
    df['Release Date'] = pd.to_datetime(df['Release Date'])
    df['Date Rated'] = pd.to_datetime(df['Date Rated'])
    df['Diff in ratings'] = round(df['IMDb Rating'] - df['Your Rating'],1)
    df['Link'] = '<a href=”' + df['URL'].astype(str) +'”>'+ df['Title'].astype(str) 
    decade_date_range = range(math.floor(df['Year'].min()/10) * 10, datetime.date.today().year + 11, 10)
    decade_date_labels = [str(i) + "'s" for i in list(decade_date_range)[:len(list(decade_date_range))-1]]
    # - to get a value to sort the df on
    decade_mapping = dict(zip(decade_date_labels, list(decade_date_range)[:len(list(decade_date_range))-1]))
    df['Decade'] = pd.cut(df['Year'], bins=list(decade_date_range), labels=decade_date_labels, 
                            include_lowest=True, right=False)
    df[['Genre 1', 'Genre 2', 'Genre 3']] = df['Genres'].str.split(', ').apply(pd.Series)[[0,1,2]]
    df['Days not rated'] = (df['Date Rated'] - df['Release Date']).dt.days

    df.drop('Title Type', axis=1, inplace=True)

    # - Create genre breakdown
    # * df_g adds multiple rows for each genre that a movie is
    df_g = df.copy()
    df_g['Genres'] = df_g['Genres'].str.split(', ')
    df_g = df_g.explode('Genres')
    df_g = df_g.rename({'Genres':'Genre'}, axis='columns')
    df_g['Category'] = df_g['Decade'].astype(str) + ' ' + df_g['Genre'].astype(str)
    genre_counts = df_g['Genre'].value_counts()
    # // agg_cols = ['Genre', 'Decade', 'Your Rating', 'IMDb Rating', 'Diff in ratings']
    # // g_mean = df_g.groupby(['Genre', 'Decade']).mean().reset_index()[agg_cols].round({'Your Rating':2,'IMDb Rating':1,'Diff in ratings':2})

    # - Adding top 5 genres as one hot encoded columns to the df
    one_hot = df['Genres'].str.get_dummies(sep=', ')
    top_5_genres = genre_counts.index[:5]
    one_hot = one_hot[top_5_genres]
    df = df.join(one_hot)

    return df, df_g, one_hot, top_5_genres


#%%
df, df_g, one_hot, top_5_genres = imdb_data()

#%%
# * Plotly color lists
color_list = ['#1A4D94', '#007A33', '#CB4F0A', '#5A2D81'] * int(len(df)/3)
full_color_list = ['#1A4D94', '#5C7DAA', '#007A33', '#33955C', '#CB4F0A', '#F58426','#5A2D81', '#DFAEE6'] * int(len(df)/7)

alt_greys = ['#cccccc', '#e4e4e4'] * len(df)


# %%
# - Table1
# todo See if links work when exporting as picture and .html file
my_ratings = pd.DataFrame()
my_ratings['My Rating'] = [i for i in range(10,0,-1)]
my_ratings['Criteria'] = ['Perfect','Great','Really good','Good','Okay','Average','Not good','Really not good','Bad','Really Bad']
my_ratings['Title'] = ['The Dark Knight',
'Inglourious Basterds',
'The Wolf of Wall Street',
'Ready Player One',
'Limitless',
'Masterminds',
'The Lobster',
'Fahrenheit 451 (2018)',
'The Room',
'Color Out Of Space'
]


fig = go.Figure(data=[go.Table(
    header=dict(values=['My Rating', 'Criteria', 'Example'],
                fill_color='#5C7DAA',
                font_color='white',
                align='left'),
    cells=dict(values=[my_ratings['My Rating'], my_ratings['Criteria'], my_ratings['Title']],
                fill_color=[alt_greys[:len(df)]]*3,
                font_color='black',
                align='left'))])

fig.update_layout(
    title=dict(
        text='How I breakdown my ratings',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    width=600,
    height=500
)



if show_all:
    fig.show()

if update_layouts:
    chart_studio.plotly.plot(fig, filename='My iMDB Rating guide', auto_open=False)

#%%
# - my rating, imdb rating histogram
# * could try to fix the hovertemplate with the binning
fig = go.Figure()

fig.add_trace(go.Histogram(x=df['Your Rating'],
                            name='My Rating',
                            hovertemplate=
                                'I gave a %{y}/' + str(len(df)) + ' movies a rating of %{x}<extra></extra>'))
fig.add_trace(go.Histogram(x=df['IMDb Rating'].apply(lambda x: math.floor(x*2)/2),
                            name='IMDb Rating',
                            hovertemplate=
                                '%{y}/' + str(len(df)) + ' of the movies that I rated <br>have an IMDb rating of %{x}' +
                                ' to .4 points higher<extra></extra>'))

fig.update_layout(barmode='overlay',
    title=dict(
            text='Distribution of my ratings and IMDb ratings',
            font=dict(
                size=24,
                color='#000000'
            ),
            x=.5
        ),
    xaxis=dict(
        title='Rating',
        tickvals=[i for i in range(1,11)]
    ),
    yaxis=dict(
        title='Count',
        tickvals=[i if i != 0 else '' for i in range(0,len(df),10)]
    ),
    width=700,
    height=500)

fig.update_traces(opacity=0.75)

if show_all:
    fig.show()

if update_layouts:
    chart_studio.plotly.plot(fig, filename='Distribution of my ratings and IMDb ratings', auto_open=False)


# %%
# - Scatter1
# - my rating vs. imdb rating

rated = df.sort_values('Date Rated',ascending=False).head(25).copy()
released = df.sort_values('Release Date',ascending=False).head(25).copy()

fig = go.Figure()

fig.add_trace(go.Scatter(x=df['IMDb Rating'],
                            y=df['Your Rating'],
                            mode='markers',
                            marker=dict(
                                size=8,
                                color=df['Year'],
                                colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,122,51)']],
                                showscale=True,
                                colorbar=dict(
                                    title="Year released"
                                ),
                                cmin=df['Year'].min(),
                                cmax=df['Year'].max(),
                                cmid=df['Year'].mean()
                            ),
                            hovertemplate=df['Title'].astype(str)+' (' +df['Year'].astype(str) + ' film)'+
                            '<br><b>IMDb Rating</b>: %{x}<br>'+
                            '<b>My Rating</b>: %{y}'+'<extra></extra>'
                            ))

fig.add_trace(go.Scatter(x=rated['IMDb Rating'],
                            y=rated['Your Rating'],
                            mode='markers',
                            marker=dict(
                                size=8,
                                color=rated['Year'],
                                colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,122,51)']],
                                showscale=True,
                                colorbar=dict(
                                    title="Year released"
                                ),
                                cmin=df['Year'].min(),
                                cmax=df['Year'].max(),
                                cmid=df['Year'].mean()
                            ),
                            hovertemplate=rated['Title'].astype(str)+' (' +rated['Year'].astype(str) + ' film)'+
                            '<br><b>IMDb Rating</b>: %{x}<br>'+
                            '<b>My Rating</b>: %{y}<br>'+
                            '<b>Date Rated</b>: '+ rated['Date Rated'].dt.strftime("%B %-d '%y") +
                            '<extra></extra>'
                            ))

fig.add_trace(go.Scatter(x=released['IMDb Rating'],
                            y=released['Your Rating'],
                            mode='markers',
                            marker=dict(
                                size=8,
                                color=released['Year'],
                                colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,122,51)']],
                                showscale=True,
                                colorbar=dict(
                                    title="Year released"
                                ),
                                cmin=df['Year'].min(),
                                cmax=df['Year'].max(),
                                cmid=df['Year'].mean()
                            ),
                            hovertemplate=released['Title'].astype(str)+' (' +released['Year'].astype(str) + ' film)'+
                            '<br><b>IMDb Rating</b>: %{x}<br>'+
                            '<b>My Rating</b>: %{y}<br>'+
                            '<b>Date Released</b>: '+ released['Date Rated'].dt.strftime("%B %-d '%y") +
                            '<extra></extra>'
                            ))


fig.update_layout(
    showlegend=False,
    updatemenus=[
        dict(
            type = "buttons",
            buttons=list([
                dict(
                    args=[dict(visible=[True, False, False])
                            ],
                    label="All ratings",
                    method="update"
                ),
                dict(
                    args=[dict(visible=[False, True, False])
                            ],
                    label="Most recently rated",
                    method="update"
                ),
                dict(
                    args = [dict(visible=[False, False, True])
                            ],
                    label="Most recently released",
                    method="update"
                )
            ]),
            direction='left',
            showactive=False,
            x=0,
            y=-.3,
            xanchor="left",
            yanchor="bottom"
        ),
    ],
    plot_bgcolor='#cccccc',
    title=dict(
        text='IMDb Rating vs. My Rating',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='IMDb Rating',
        range=[.5,10.5],
        tickvals=[i for i in range(1,11)]
    ),
    yaxis=dict(
        title='My Rating',
        range=[.5,10.5],
        tickvals=[i for i in range(1,11)]
    ),
    width=600,
    height=500,
    shapes=[dict(type='line',
                    x0=0,
                    y0=0,
                    x1=10,
                    y1=10,
                line=dict(
                    color='black',
                    width=2
                ))],
    annotations=[
            go.layout.Annotation(
                text='Movies I liked<br>more than IMDb',
                align='center',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=.15,
                y=0.75,
                bordercolor='black',
                borderwidth=1
            ),
            go.layout.Annotation(
                text='Movies I liked<br>less than IMDb',
                align='center',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=.91,
                y=.15,
                bordercolor='black',
                borderwidth=1
            )
        ]
)



if show_all:
    fig.show()

if update_layouts:
    chart_studio.plotly.plot(fig, filename='IMDb Rating vs. My Rating', auto_open=False)


# %%
# - Table2
df_diff = df.sort_values(axis=0,by='Diff in ratings').reset_index(drop=True).copy()
df_diff['T_Title'] = df_diff['Title'].astype(str) + ' (' + df_diff['Year'].astype(str) + ' film)'

colors = n_colors('rgb(0,122,51)','rgb(207, 198, 0)', int(len(df_diff)/2), colortype='rgb') + n_colors('rgb(207, 198, 0)', 'rgb(0, 145, 222)', int(len(df_diff)/2), colortype='rgb')
fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>Title</b>', '<b>IMDb Rating</b>', '<b>My Rating</b>', '<b>Difference in Ratings</b>'],
    align='center',font=dict(color='white', size=12),
    fill_color='#5C7DAA'
  ),
  cells=dict(
    values=[df_diff['T_Title'], df_diff['IMDb Rating'], df_diff['Your Rating'], round(df_diff['Diff in ratings'],1)],
    align='left', font=dict(color=['black', 'black', 'black', 'white'], size=11),
    fill_color=[alt_greys[:len(df_diff)],alt_greys[:len(df_diff)],alt_greys[:len(df_diff)],colors]
    ))
])

fig.update_layout(
    title=dict(
        text='IMDb Rating vs. My Rating breakdown',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    width=600,
    height=600)



if show_all:
    fig.show()

if update_layouts:
    chart_studio.plotly.plot(fig, filename='IMDb Rating vs. My Rating breakdown', auto_open=False)


# %%
# - Scatter2
# - year vs diff in ratings
# todo toggle by genres (buttons)
fig = go.Figure(data=go.Scatter(x=df['Year'],
                    y=df['Diff in ratings'],
                    mode='markers',
                    # marker_color=df['Runtime (mins)'],
                    marker=dict(
                        size=8,
                        color=df['Your Rating'],
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(26,77,148)']],
                        showscale=True,
                        colorbar=dict(
                            title="My rating"
                        ),
                        cmin=df['Your Rating'].min(),
                        cmax=df['Your Rating'].max(),
                        cmid=df['Your Rating'].mean()
                    ),
                    hovertemplate=df['Title'].astype(str)+' (' +df['Year'].astype(str) + ' film)'+
                    '<br><b>IMDb Rating</b>: '+df['IMDb Rating'].astype(str)+'<br>'+
                    '<b>My Rating</b>: '+df['Your Rating'].astype(str)+'<br>'+
                    '<b>Difference</b>: %{y}'+'<extra></extra>'
                ))
fig.update_layout(
    plot_bgcolor='#cccccc',
    title=dict(
        text='Year vs. Difference in Ratings',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Year',
        range=[df['Year'].min() - 1, df['Year'].max() + 1]
    ),
    yaxis=dict(
        title='Difference in Ratings',
        range=[math.ceil(df['Diff in ratings'].max()), math.floor(df['Diff in ratings'].min())],
        tickvals=[i for i in range(math.floor(df['Diff in ratings'].min()),
                                    math.ceil(df['Diff in ratings'].max()))]
    ),
    width=600,
    height=500,
    shapes=[dict(type='line',
                    x0=0,
                    y0=0,
                    x1=df['Year'].max(),
                    y1=0,
                    line=dict(
                        color='black',
                        width=2
                    ))],
    annotations=[
            go.layout.Annotation(
                text='Movies I liked<br>more than IMDb',
                align='center',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=.15,
                y=.85,
                bordercolor='black',
                borderwidth=1
            ),
            go.layout.Annotation(
                text='Movies I liked<br>less than IMDb',
                align='center',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=.15,
                y=.185,
                bordercolor='black',
                borderwidth=1
            )
        ]

)

if show_all:
    fig.show()

if update_layouts:
    chart_studio.plotly.plot(fig, filename='Year vs. Difference in Ratings', auto_open=False)


# %%
# - bar1
# - num movies per year
bar = df.groupby('Year').count()['Title'].copy()
fig = go.Figure(data=go.Bar(x=bar.index,
                    y=bar.values,
                    marker_color=full_color_list[0:len(bar)],
                    hovertemplate='Year: ' + bar.index.astype(str) + ''+
                    '<br>Count: '+ bar.values.astype(str) +'<br>'
                    + '<extra></extra>'
                ))
fig.update_layout(
    plot_bgcolor='#cccccc',
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
    ),
    width=700,
    height=500

)

if show_all:
    fig.show()

if update_layouts:
    chart_studio.plotly.plot(fig, filename='Number of movies in my ratings by year released', auto_open=False)


# %%
# - Table3
# - top 5 genres by decade

# fig.update_layout(
#     title=dict(
#         text='How I breakdown my ratings',
#         font=dict(
#             size=24,
#             color='#000000'
#         ),
#         x=.5
#     ))


# %%
# - plotly box/whisker1
# - x is decade y is my rating

df.sort_values('Year', inplace=True)
fig = go.Figure(data=go.Box(x=df['Decade'],
                    y=df['Your Rating'],
                    marker=dict( 
                        color='#000000'
                    ),
                    line=dict(color='#CB4F0A')
                ))
fig.update_layout(
    plot_bgcolor='#cccccc',
    title=dict(
        text='Distribution of my ratings by decade',
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
        title='My Rating'
    ),
    width=700,
    height=500

)

if show_all:
    fig.show()

if update_layouts:
    chart_studio.plotly.plot(fig, filename='Distribution of my ratings by decade', auto_open=False)


# %%
# - plotly box/whisker2
# - x is genre y is my rating
# todo update with new genre handling
# todo change hovertext
# todo Add mean

fig = go.Figure()
for i in range(len(top_5_genres)):
    fig.add_trace(go.Box(
        y=df[df[top_5_genres[i]] == 1]['Your Rating'],
        name=top_5_genres[i]
    ))
fig.update_layout(
    plot_bgcolor='#cccccc',
    title=dict(
        text='Distribution of my ratings by genre',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Genre'
    ),
    yaxis=dict(
        title='My Rating'
    ),
    width=700,
    height=500

)

if show_all:
    fig.show()

if update_layouts:
    chart_studio.plotly.plot(fig, filename='Distribution of my ratings by genre', auto_open=False)

#%%
# - grid of top genres and decades scatterplot

num_plots = 3
colors = ['blue', 'purple', 'red', 'green', 'orange']
symbols = ['circle', 'cross', 'diamond', 104, 105]

fig = make_subplots(rows=num_plots, cols=num_plots,
                    vertical_spacing=0.05, horizontal_spacing=0.05,
                    subplot_titles=[j + ' ' + i for j in df['Decade'].value_counts()[:num_plots].index for i in top_5_genres[:num_plots]])

for decade, row, color in zip(df['Decade'].value_counts()[:num_plots].index, range(1, num_plots + 1), colors[:num_plots]):
    for genre, col, shape in zip(top_5_genres[:num_plots], range(1, num_plots + 1), symbols[:num_plots]):
        fig.add_trace(
            go.Scatter(x=df[(df['Decade'] == decade) & (df[genre] == True)]['Your Rating'], 
                    y=df[(df['Decade'] == decade) & (df[genre] == True)]['IMDb Rating'],
                    mode='markers', marker_color=color, marker_symbol=shape, marker_size=8,
                    hovertemplate=df[(df['Decade'] == decade) & (df[genre] == True)]['Title'].astype(str)+' (' 
                    +df[(df['Decade'] == decade) & (df[genre] == True)]['Year'].astype(str) + ' film)'+
                    '<br><b>IMDb Rating</b>: '+df[(df['Decade'] == decade) & (df[genre] == True)]['IMDb Rating'].astype(str)+'<br>'+
                    '<b>My Rating</b>: '+df[(df['Decade'] == decade) & (df[genre] == True)]['Your Rating'].astype(str)+'<br>'+
                    '<b>Difference</b>: %{y}'+'<extra></extra>'),
            row=row, col=col
        )

        # print(df[(df['Decade'] == decade) & (df[genre] == True)]['Your Rating'].corr(df[(df['Decade'] == decade) & (df[genre] == True)]['IMDb Rating']))

        if row == num_plots and col == 1:
            fig.update_xaxes(title_text='My Rating', range=[-0.5, 10.5], row=row, col=col)
            fig.update_yaxes(title_text='IMDb Rating', range=[-0.5, 10.5], row=row, col=col)
        else:
            fig.update_xaxes(range=[-0.5, 10.5], row=row, col=col, showticklabels=False)
            fig.update_yaxes(range=[-0.5, 10.5], row=row, col=col, showticklabels=False)

for i in fig['layout']['annotations']:
    i['font']['size'] = 12

fig.update_layout(height=500, width=700, showlegend=False, title_text="Top Genres and Decades")

if show_all:
    fig.show()

if update_layouts:
    chart_studio.plotly.plot(fig, filename='Top Genres and Decades', auto_open=False)


#%%
# - genre box plot
# - y is rating x is decade
# - filter on genres
# todo dynamically add genres from genre_counts
# todo add title
# todo toggle between my rating/imdb rating


fig = go.Figure()

# - Dynamically add traces
# for i in genre_counts:
#     fig.add_trace(go.Box(
#         y=df_g[df_g['Genre'] == i]['Your Rating'],
#         name=i
#     ))

# ! hover template doesn't really work
fig.add_trace(go.Box(
        y=df_g[df_g['Genre'] == 'Comedy']['Your Rating'],
        x=df_g[df_g['Genre'] == 'Comedy']['Decade'],
        # hovertemplate=df_g[df_g['Genre'] == 'Comedy']['Title'].astype(str)+
        #             ' (' +df_g[df_g['Genre'] == 'Comedy']['Year'].astype(str) + ' film)'+
        #             '<br><b>IMDb Rating</b>: '+df_g[df_g['Genre'] == 'Comedy']['IMDb Rating'].astype(str)+'<br>'+
        #             '<b>My Rating</b>: %{y}<br>'+
        #             '<b>Difference</b>: '+ df_g[df_g['Genre'] == 'Comedy']['Diff in ratings'].astype(str)+'<extra></extra>',
        name='Comedy',
        boxpoints='all',
        jitter=.25,
        pointpos=-1.8,
        # - make first trace visible
        visible = True
    ))

fig.add_trace(go.Box(
        y=df_g[df_g['Genre'] == 'Drama']['Your Rating'],
        x=df_g[df_g['Genre'] == 'Drama']['Decade'],
        # hovertemplate=df_g[df_g['Genre'] == 'Drama']['Title'].astype(str)+
        #             ' (' +df_g[df_g['Genre'] == 'Drama']['Year'].astype(str) + ' film)'+
        #             '<br><b>IMDb Rating</b>: '+df_g[df_g['Genre'] == 'Drama']['IMDb Rating'].astype(str)+'<br>'+
        #             '<b>My Rating</b>: %{y}<br>'+
        #             '<b>Difference</b>: '+ df_g[df_g['Genre'] == 'Drama']['Diff in ratings'].astype(str)+'<extra></extra>',
        name='Drama',
        boxpoints='all',
        jitter=.25,
        pointpos=-1.8,
        visible = False
    ))

fig.update_layout(
    xaxis=dict(
        title='Decade'
    ),
    yaxis=dict(
        title='Your Rating',
        range=[0,11]
    ),
    updatemenus=[
        dict(
            buttons=list([
                dict(label="Comedy",
                     method="update",
                     args=[{"visible": [True, False]},
                           {"title": "Comedy"}]),
                dict(label="Drama",
                     method="update",
                     args=[{"visible": [False, True]},
                           {"title": "Drama"}])
            ]),
        )
    ])

if show_all:
    fig.show()

#%%
# todo My 10's/9's
# - y is number of votes
# - x is IMDb rating
# - fitler by genre?


# %%
# todo Change to plt bar
# df.groupby('Decade').sum()[['Sci-Fi', 'Crime', 'Comedy', 'Action', 'Thriller']].plot(kind='bar')
# - eh idk
# - Maybe do averages? or box plot


# %%
# todo grid of genre and decade correlations
# * at least 10 records to get meaningful data

# - do 4x4 correlation grid with titles
#! need to use df_g for this now

min_recs = 10
gen_records = df_g.groupby(['Genre', 'Decade']).count().reset_index()[df_g.groupby(['Genre', 'Decade']).count().reset_index()['Title'] >= min_recs][['Genre', 'Decade']]

# popular_genres = df_g['Genres'].value_counts()[df_g['Genres'].value_counts().values >= 15].index
# - or df_g['Genres'].value_counts().head().index
dict_list = []
for i, j in gen_records.itertuples(index=False):
    column_1 = df_g[(df_g['Decade'] == j) & (df_g['Genre'] == i)]['Your Rating']
    column_2 = df_g[(df_g['Decade'] == j) & (df_g['Genre'] == i)]['IMDb Rating']
    dict_list.append({'Decade': i, 'Genre': j, 'Correlation': column_1.corr(column_2)})

df_corr = pd.DataFrame.from_dict(dict_list).sort_values('Correlation', ascending=False).reset_index(drop=True)
