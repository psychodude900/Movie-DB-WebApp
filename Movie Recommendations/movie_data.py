import requests
import pandas as pd
from tmdbv3api import *
import json
import inspect

tmdb = TMDb()
tmdb.api_key = "89742783d142cd168d83e3f5f08cb864"

"""
source_code = inspect.getsource(Movie)
print(source_code)
"""

genres_url = "https://api.themoviedb.org/3/genre/movie/list?api_key=89742783d142cd168d83e3f5f08cb864"

access_url = "https://api.themoviedb.org/3%s?api_key=89742783d142cd168d83e3f5f08cb864"


headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4OTc0Mjc4M2QxNDJjZDE2OGQ4M2UzZjVmMDhjYjg2NCIsInN1YiI6IjY0YjFiOGI1Mzc4MDYyMDBlMmFhNDNkYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kZIqLLDHBJh2tyFBAFt59e6ksfgzTWaHUTsqgHSI2PM"
}

urls = {
        "details": "/movie/%s",
        "alternative_titles": "/movie/%s/alternative_titles",
        "changes": "/movie/%s/changes",
        "credits": "/movie/%s/credits",
        "external_ids": "/movie/%s/external_ids",
        "images": "/movie/%s/images",
        "keywords": "/movie/%s/keywords",
        "lists": "/movie/%s/lists",
        "reviews": "/movie/%s/reviews",
        "videos": "/movie/%s/videos",
        "recommendations": "/movie/%s/recommendations",
        "latest": "/movie/latest",
        "now_playing": "/movie/now_playing",
        "top_rated": "/movie/top_rated",
        "upcoming": "/movie/upcoming",
        "popular": "/movie/popular",
        "search_movie": "/search/movie",
        "search_tv": "/search/tv",
        "similar": "/movie/%s/similar",
        "external": "/find/%s",
        "release_dates": "/movie/%s/release_dates",
        "watch_providers": "/movie/%s/watch/providers",
        "image": "https://image.tmdb.org/t/p/w500"
}

genres_df = pd.DataFrame(json.loads(requests.get(genres_url, headers=headers).text)["genres"])

discover_queries = {
    "adult content": "include_adult=",
    "language": "language=",
    "page": "page=",
    "release year": "year=",
    "sort": "sort-by=",
    "rating <=": "vote_average.lte=",
    "rating >=": "vote_average.gte=",
    "rating count >=": "vote_count.gte=",
    "rating count <=": "vote_average.lte=",
}


def get_genre_id(genre):
    genre_id = genres_df[genres_df["name"] == genre]["id"]
    return genre_id.iloc[0]


def get_genre_name(id):
    genre_name = genres_df[genres_df["id"] == id]["name"]
    return genre_name.iloc[0]


def search(name):
    query = "&query="+name
    page_data = json.loads(requests.get(access_url % urls["search_movie"] + query, headers=headers).text)
    pages = page_data["total_pages"]
    results = []
    for x in range(1, pages+1):
        url = access_url % urls["search_movie"] + query + "&page=" + str(x)
        movies = json.loads(requests.get(url, headers=headers).text)
        for movie in movies["results"]:
            genres = []
            if movie["vote_count"] >= 100:
                for genre in movie["genre_ids"]:
                    genres.append(get_genre_name(genre))
                movie_result = {
                    "Title": movie["title"],
                    "Genres": " ".join(genre for genre in genres),
                    "Release date": movie["release_date"],
                    "Rating": str(movie["vote_average"]),
                    "Overview": movie["overview"],
                    "Movie Poster": movie["poster_path"]
                }
                results.append(movie_result)
    return results


def discover():
    pass

