# imdbratings

This project is for me to look a little bit more at my imdb ratings. Eventually, I'd like to create a Plotly/Dash dashboard that summarizes the data just like in ethanfuerst/[spotifyinsights](https://github.com/ethanfuerst/spotifyinsights)

## Files in this repository

__*ratings_analysis.py*__ - .py file that takes data from the ratings.csv and creates the visualizations

__*ratings.csv*__ - .csv file with my ratings data.

__*ratings_clean.csv*__ - .csv file connected to the .twb

__*rating_vis.twb*__ - Tableau workbook where I can plan out how I want to visualize the data

__*.gitignore*__ - shows github what files to ignore when I commit my changes.

## TODO

- [x] one hot encoding for genres
  - [ ] Figure out threshold of records for the ML model (for one-hot columns, what is the number of records that each column must contain when compared to the length of the df. Is it 10 percent?)
- [ ] Bin columns
- [ ] look in to [APIs](http://www.omdbapi.com/)
- [ ] learn more about Plotly and Dash and create visualizations
- [ ] create ML model to predict my scores
