import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import math
from imdb_data import get_imdb_data

df = get_imdb_data()
genre_counts = df.explode('genre_list')['genre_list'].value_counts()
top_5_genres = genre_counts.index[:5]
all_genres = ['All Genres'] + list(genre_counts.index)
center_style = {'textAlign': 'center'}

def genre_finder(x, g1, g2):
    if 'All Genres' in [g1, g2]:
        return True
    elif g1 == g2:
        return g1 in x
    elif g2 == '':
        return g1 in x
    else:
        return (g1 in x) and (g2 in x)

datatable_params = dict(
    style_header = {
        'backgroundColor': '#A8A8A8',
        'fontWeight': 'bold',
        'border': '1px solid black',
        'whiteSpace': 'normal'
    },
    style_cell = {
        'font-family':'sans-serif',
        'backgroundColor': '#D3D3D3',
        'textAlign': 'center',
        'border': '1px solid grey',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis'
    },
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px'
    }
    )

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.layout = html.Div([
    dbc.Row(
        html.H1(
            children='My IMDb Ratings Dashboard',
            style=center_style)
    ),
    dbc.Row(
        html.H2(
            children='Use the dropdowns below to sort by genre!',
            style=center_style
        )
    ),
    html.Div([
        dcc.Dropdown(
            id='genre1',
            options=[{
                'label': i, 
                'value': i
            } for i in all_genres],
            value='All Genres'
        )
    ],
    style={
        'width': '25%',
        'padding-left':'25%',
        'display': 'inline-block',
        'textAlign': 'center'
    }),

    html.Div([
        dcc.Dropdown(
            id='genre2',
            options=[{
                'label': '',
                'value': ''
            }] + [{
                    'label': i, 
                    'value': i
            } for i in all_genres],
            value=''
        )
    ],
    style={
        'width': '25%',
        'padding-right':'25%',
        'float': 'right',
        'display': 'inline-block',
        'textAlign': 'center'
    }),
    
    html.Center([
        html.Div([
            dt.DataTable(
                id='breakdown_table',
                columns=[{
                    "name": i, 
                    "id": i
                } for i in ['My Rating', 'Criteria', 'Example']],
                **datatable_params,
                style_table = {
                    'overflowX': 'scroll',
                    'maxWidth': '80%',
                    'minWidth': '40%'
                },
            )
        ])
    ]),

    html.Center(
        [dcc.Graph(id='hist1')]
    ),

    html.Center(
        [dcc.Graph(id='scatter1')]
    ),
    
    html.Center(
        [dcc.Graph(id='scatter2')]
    ),

    html.Center(
        [dcc.Graph(id='boxplot1')]
    ),

    html.Center([
        html.Div([
            dt.DataTable(
                id='allmovies_table',
                columns=[
                    {
                    "name": 'Title', 
                    "id": 'Title'
                    },
                    {
                    "name": 'Link', 
                    "id": 'Link',
                    'type':'text',
                    'presentation':'markdown'
                }] + [{
                    "name": i, 
                    "id": i
                } for i in ['My Rating', 'IMDb Rating', 'Difference in Ratings',
                            'Year', 'Genres', 'Director', 'Date Released', 'Date Rated']],
                **datatable_params,
                style_table = {
                    'overflowX': 'auto',
                    'maxWidth': '80%',
                    'minWidth': '40%',
                    'height': '750px',
                    'overflowY': 'auto'
                },
                filter_action="native",
                sort_action="native",
                sort_mode="multi"
            )
        ])
    ]),

    # 4x4 scatterplot grid

    # genre boxplot2
])


@app.callback(
    Output('breakdown_table', 'data'),
    [
        Input('genre1', 'value'),
        Input('genre2', 'value')
    ]
)
def update_ratings_breakdown_table(genre1, genre2):
    mask = df['genre_list'].apply(lambda x: genre_finder(x, g1=genre1, g2=genre2))
    sample_movies = df[mask]

    examples = pd.DataFrame(columns=['My Rating', 'Criteria', 'Example'])
    examples['My Rating'] = [i for i in range(10, 0, -1)]
    examples['Criteria'] = ['Perfect','Great','Really good','Good','Okay','Average',
                            'Not good','Really not good','Bad','Really Bad']

    def get_sample_movie(row):
        if len(sample_movies[sample_movies['Your Rating'] == row['My Rating']]) == 0:
            return ''
        else:
            return sample_movies[sample_movies['Your Rating'] == row['My Rating']].sample(1).iloc[0]['Title']
    
    examples['Example'] = examples.apply(get_sample_movie, axis=1)

    return examples.to_dict('rows')

@app.callback(
    Output('hist1', 'figure'),
    [
        Input('genre1', 'value'),
        Input('genre2', 'value')
    ]
)
def update_hist1(genre1, genre2):
    mask = df['genre_list'].apply(lambda x: genre_finder(x, g1=genre1, g2=genre2))
    movies = df[mask]

    return {
        'data': [
            go.Histogram(x=movies['Your Rating'],
                xbins=dict(
                    start=.5,
                    end=10.5,
                    size=1
                ),
                name='My Rating',
                opacity=0.75,
                hovertemplate='I gave a %{y}/' + str(len(movies)) + 
                    ' movies a rating of %{x}<extra></extra>'
            ),
            go.Histogram(
                x=movies['IMDb Rating'].round(0),
                xbins=dict(
                    start=.5,
                    end=10.5,
                    size=1
                ),
                name='IMDb Rating (rounded)',
                opacity=0.75,
                hovertemplate='%{y}/' + str(len(movies)) + 
                    ' of the movies that I rated <br>have an IMDb rating of %{x}' +
                    '<extra></extra>'
            )
        ],
        'layout': go.Layout(
            barmode='overlay',
            plot_bgcolor='#D3D3D3',
            width=1000,
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
                tickvals=[i for i in range(1,11)],
                range=[0,11]
            ),
            yaxis=dict(
                title='Count',
                tickvals=[i if i != 0 else '' for i in range(0,len(movies),10)]
            )
        )
    }

@app.callback(
    Output('scatter1', 'figure'),
    [
        Input('genre1', 'value'),
        Input('genre2', 'value')
    ]
)
def update_scatter1(genre1, genre2):
    mask = df['genre_list'].apply(lambda x: genre_finder(x, g1=genre1, g2=genre2))
    movies = df[mask]
    rated = movies.sort_values('Date Rated',ascending=False).head(10).copy()
    released = movies.sort_values('Release Date',ascending=False).head(10).copy()

    marker_format = dict(
        size=8,
        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,122,51)']],
        showscale=True,
        colorbar=dict(
            title="Year released"
        ),
        cmin=movies['Year'].min(),
        cmax=movies['Year'].max(),
        cmid=movies['Year'].mean()
    )

    return {
        'data': [
            go.Scatter(
                x=movies['IMDb Rating'],
                y=movies['Your Rating'],
                mode='markers',
                marker={**marker_format,  **{'color':movies['Year']}},
                hovertemplate=movies['Title'].astype(str)+' (' +movies['Year'].astype(str) + ' film)'+
                '<br><b>IMDb Rating</b>: %{x}<br>'+
                '<b>My Rating</b>: %{y}'+'<extra></extra>'
            ),
            go.Scatter(
                x=rated['IMDb Rating'],
                y=rated['Your Rating'],
                mode='markers',
                marker={**marker_format,  **{'color':rated['Year']}},
                hovertemplate=rated['Title'].astype(str)+' (' +rated['Year'].astype(str) + ' film)'+
                '<br><b>IMDb Rating</b>: %{x}<br>'+
                '<b>My Rating</b>: %{y}<br>'+
                '<b>Date Rated</b>: '+ rated['Date Rated'].dt.strftime("%B %-d '%y") +
                '<extra></extra>'
            ),
            go.Scatter(
                x=released['IMDb Rating'],
                y=released['Your Rating'],
                mode='markers',
                marker={**marker_format,  **{'color':released['Year']}},
                hovertemplate=released['Title'].astype(str)+' (' +released['Year'].astype(str) + ' film)'+
                '<br><b>IMDb Rating</b>: %{x}<br>'+
                '<b>My Rating</b>: %{y}<br>'+
                '<b>Date Released</b>: '+ released['Date Rated'].dt.strftime("%B %-d '%y") +
                '<extra></extra>'
            )
        ],
        'layout': go.Layout(
            showlegend=False,
            hovermode='closest',
            updatemenus=[
                dict(
                    type = "buttons",
                    buttons=list([
                        dict(
                            args=[
                                dict(visible=[True, False, False])
                            ],
                            label="All ratings",
                            method="update"
                        ),
                        dict(
                            args=[
                                dict(visible=[False, True, False])
                            ],
                            label="Most recently rated",
                            method="update"
                        ),
                        dict(
                            args = [
                                dict(visible=[False, False, True])
                            ],
                            label="Most recently released",
                            method="update"
                        )
                    ]),
                    direction='left',
                    showactive=False,
                    x=.5,
                    y=-.25,
                    xanchor="center",
                    yanchor="bottom"
                ),
            ],
            plot_bgcolor='#D3D3D3',
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
            width=750,
            height=750,
            shapes=[
                dict(
                    type='line',
                    x0=0, y0=0,
                    x1=10, y1=10,
                    line=dict(
                        color='black',
                        width=2
                    )
                )
            ],
            annotations=[
                go.layout.Annotation(
                    text=title,
                    align='center',
                    showarrow=False,
                    xref='x',
                    yref='y',
                    x=x_coord,
                    y=y_coord,
                    bordercolor='black',
                    borderwidth=1
                ) for title, x_coord, y_coord in zip(
                    ['Movies I liked<br>more than IMDb', 
                    'Movies I liked<br>less than IMDb'],
                    [2.5, 8.5],
                    [8.5, 2.5]
                )
            ]
        )
    }

@app.callback(
    Output('scatter2', 'figure'),
    [
        Input('genre1', 'value'),
        Input('genre2', 'value')
    ]
)
def update_scatter2(genre1, genre2):
    mask = df['genre_list'].apply(lambda x: genre_finder(x, g1=genre1, g2=genre2))
    movies = df[mask]

    year_range = movies['Year'].max() - movies['Year'].min()

    return {
        'data': [
            go.Scatter(
                x=movies['Year'],
                y=movies['Diff in ratings'],
                mode='markers',
                # marker_color=movies['Runtime (mins)'],
                marker=dict(
                    size=8,
                    color=movies['Your Rating'],
                    colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(26,77,148)']],
                    showscale=True,
                    colorbar=dict(
                        title="My rating"
                    ),
                    cmin=movies['Your Rating'].min(),
                    cmax=movies['Your Rating'].max(),
                    cmid=movies['Your Rating'].mean()
                ),
                hovertemplate=movies['Title'].astype(str)+' (' +movies['Year'].astype(str) + ' film)'+
                '<br><b>IMDb Rating</b>: '+movies['IMDb Rating'].astype(str)+'<br>'+
                '<b>My Rating</b>: '+movies['Your Rating'].astype(str)+'<br>'+
                '<b>Difference</b>: %{y}'+'<extra></extra>'
            )
        ],
        'layout': go.Layout(
            hovermode='closest',
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
                range=[movies['Year'].min() - 1, movies['Year'].max() + 1]
            ),
            yaxis=dict(
                title='Difference in Ratings',
                range=[math.ceil(movies['Diff in ratings'].max()), math.floor(movies['Diff in ratings'].min())],
                tickvals=[i for i in range(math.floor(movies['Diff in ratings'].min()),
                                            math.ceil(movies['Diff in ratings'].max()))]
            ),
            width=750,
            height=750,
            shapes=[dict(type='line',
                            x0=movies['Year'].min() - .05 * year_range,
                            y0=0,
                            x1=movies['Year'].max() + .05 * year_range,
                            y1=0,
                            line=dict(
                                color='black',
                                width=2
                            ))],
            annotations=[
                go.layout.Annotation(
                    text=title,
                    align='center',
                    showarrow=False,
                    xref='x',
                    yref='y',
                    x=x_coord,
                    y=y_coord,
                    bordercolor='black',
                    borderwidth=1
                ) for title, x_coord, y_coord in zip(
                    ['Movies I liked<br>more than IMDb', 
                    'Movies I liked<br>less than IMDb'],
                    [movies['Year'].min() + .2 * year_range, 
                    movies['Year'].min() + .2 * year_range],
                    [-.2 * (movies['Diff in ratings'].max()), .2 * (movies['Diff in ratings'].max())]
                )
            ]

        )
    }

@app.callback(
    Output('boxplot1', 'figure'),
    [
        Input('genre1', 'value'),
        Input('genre2', 'value')
    ]
)
def update_boxplot1(genre1, genre2):
    mask = df['genre_list'].apply(lambda x: genre_finder(x, g1=genre1, g2=genre2))
    movies = df[mask].sort_values('Release Date')
    decades = movies['Decade'].unique()

    colors = ['red', 'green', 'blue', 'orange', 'purple', 'yellow', 'red'] * len(decades)

    return {
        'data': [
            go.Box(
                x=movies[movies['Decade'].isin([dec])]['Decade'],
                y=movies[movies['Decade'].isin([dec])]['Your Rating'],
                marker=dict( 
                    color='#000000'
                ),
                line=dict(
                    color=col
                ),
                boxmean='sd'
            ) for dec, col in zip(
                decades,
                colors
            )
        ],
        'layout': go.Layout(
            showlegend=False,
            plot_bgcolor='#D3D3D3',
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
            width=1000
        )
    }

@app.callback(
    Output('allmovies_table', 'data'),
    [
        Input('genre1', 'value'),
        Input('genre2', 'value')
    ]
)
def update_ratings_breakdown_table(genre1, genre2):
    mask = df['genre_list'].apply(lambda x: genre_finder(x, g1=genre1, g2=genre2))
    movies = df[mask]
    
    movies['Link'] = '[Link](' + movies['URL'] + ')'

    movies = movies[['Title', 
        'Link',
        'Your Rating', 
        'IMDb Rating',
        'Diff in ratings',
        'Year',
        'Genres',
        'Directors',
        'Release Date',
        'Date Rated']].copy()
    
    movies.columns = ['Title', 'Link', 'My Rating', 'IMDb Rating', 'Difference in Ratings',
                            'Year', 'Genres', 'Director', 'Date Released', 'Date Rated']

    movies['Date Released'] = movies['Date Released'].dt.strftime('%B %-d, %Y')
    movies['Date Rated'] = movies['Date Rated'].dt.strftime('%B %-d, %Y')

    return movies.to_dict('rows')


if __name__ == '__main__':
    app.run_server(debug=True)
