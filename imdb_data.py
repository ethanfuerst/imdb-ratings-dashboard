import datetime
import math

import pandas as pd


def get_imdb_data() -> pd.DataFrame:
    df = pd.read_csv("ratings.csv")
    df = df[df["Title Type"] == "Movie"].copy()
    df = df.drop("Title Type", axis=1).copy()
    df["Release Date"] = pd.to_datetime(df["Release Date"])
    df["Date Rated"] = pd.to_datetime(df["Date Rated"])
    df["Diff in ratings"] = round(df["IMDb Rating"] - df["Your Rating"], 1)
    df["Link"] = "<a href=”" + df["URL"].astype(str) + "”>" + df["Title"].astype(str)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    min_year = int(df["Year"].dropna().min()) if not df["Year"].dropna().empty else 1900

    decade_date_range = range(
        math.floor(min_year / 10) * 10, datetime.date.today().year + 11, 10
    )
    decade_date_labels = [
        str(i) + "'s"
        for i in list(decade_date_range)[: len(list(decade_date_range)) - 1]
    ]
    df["Decade"] = pd.cut(
        df["Year"],
        bins=list(decade_date_range),
        labels=decade_date_labels,
        include_lowest=True,
        right=False,
    )
    df["genre_list"] = df["Genres"].str.split(", ")
    df["Days not rated"] = (df["Date Rated"] - df["Release Date"]).dt.days

    return df
