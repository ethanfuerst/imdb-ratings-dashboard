import pandas as pd
import math
import datetime

def get_imdb_data():
    with open('ratings.csv', 'r', encoding='mac_roman', newline='') as csvfile:
        df = pd.read_csv(csvfile)

    df = df[df['Title Type'] == 'movie'].copy()
    df = df.drop('Title Type', axis=1).copy()
    df['Release Date'] = pd.to_datetime(df['Release Date'])
    df['Date Rated'] = pd.to_datetime(df['Date Rated'])
    df['Diff in ratings'] = round(df['IMDb Rating'] - df['Your Rating'],1)
    df['Link'] = '<a href=”' + df['URL'].astype(str) +'”>'+ df['Title'].astype(str) 
    decade_date_range = range(math.floor(df['Year'].min()/10) * 10, datetime.date.today().year + 11, 10)
    decade_date_labels = [str(i) + "'s" for i in list(decade_date_range)[:len(list(decade_date_range))-1]]
    df['Decade'] = pd.cut(
        df['Year'], 
        bins=list(decade_date_range), 
        labels=decade_date_labels, 
        include_lowest=True, 
        right=False
    )
    df['genre_list'] = df['Genres'].str.split(', ')
    df['Days not rated'] = (df['Date Rated'] - df['Release Date']).dt.days
    
    return df
