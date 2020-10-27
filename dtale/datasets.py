import pandas as pd
import requests
import zipfile

from six import BytesIO


def covid():
    from dtale.cli.loaders.csv_loader import loader_func as load_csv

    data = load_csv(
        path="https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv",
        parse_dates=["date"],
    )
    codes = load_csv(
        path="https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv",
    )
    codes = codes.set_index("State").to_dict()["Abbreviation"]
    data["state_code"] = data["state"].map(codes)
    return data


def seinfeld():
    from dtale.cli.loaders.csv_loader import loader_func as load_csv

    episodes = load_csv(
        path="https://github.com/4m4n5/the-seinfeld-chronicles/raw/master/episode_info.csv"
    )
    episodes = episodes[[c for c in episodes.columns if c not in ["Unnamed: 0"]]]
    scripts = load_csv(
        path="https://github.com/4m4n5/the-seinfeld-chronicles/raw/master/scripts.csv"
    )
    scripts = scripts[
        [c for c in scripts.columns if c not in ["Unnamed: 0", "Season", "EpisodeNo"]]
    ]
    return pd.merge(episodes, scripts, how="inner", on="SEID")


def load_zip(url):
    response = requests.get(url)
    with zipfile.ZipFile(BytesIO(response.content)) as thezip:
        for zipinfo in thezip.infolist():
            yield zipinfo.filename, thezip.open(zipinfo.filename)


def simpsons():
    from dtale.cli.loaders.csv_loader import loader_func as load_csv

    episodes = load_csv(
        path="https://github.com/aschonfeld/dtale-media/raw/master/datasets/simpsons_episodes.csv"
    )
    episodes = episodes.rename(columns={"id": "episode_id"})
    _, scripts = next(
        load_zip(
            "https://github.com/aschonfeld/dtale-media/raw/master/datasets/simpsons_script_lines.csv.zip"
        )
    )
    scripts = pd.read_csv(scripts)
    return pd.merge(episodes, scripts, how="inner", on="episode_id")


def video_games():
    _, games = next(
        load_zip(
            "https://github.com/aschonfeld/dtale-media/raw/master/datasets/vgsales.csv.zip"
        )
    )
    return pd.read_csv(games)


def movies():
    _, movies = next(
        load_zip(
            "https://github.com/aschonfeld/dtale-media/raw/master/datasets/IMDb_movies.csv.zip"
        )
    )
    movies = pd.read_csv(movies)
    movies.loc[:, "year"] = (
        movies["year"].where(~(movies["year"] == "TV Movie 2019"), "2019").astype("int")
    )
    return movies


def time_dataframe():
    try:
        from pandas._testing import makeTimeDataFrame

        return makeTimeDataFrame()
    except ImportError:
        from pandas.util.testing import makeTimeDataFrame

        return makeTimeDataFrame()