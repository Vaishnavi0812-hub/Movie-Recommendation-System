import pandas as pd
import numpy as np
import requests
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("data\movies.csv")

# TMDb API Key
API_KEY = "e588fc141b95bf18111a19119c28c21b"  # Replace with your actual TMDb API Key
BASE_URL = "https://api.themoviedb.org/3"

def get_genre_map():
    """Fetches genre mapping from TMDb API."""
    try:
        url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
        response = requests.get(url).json()
        return {genre["id"]: genre["name"] for genre in response.get("genres", [])}
    except Exception as e:
        print(f"Error fetching genre mapping: {e}")
        return {}

# Get genre mapping
GENRE_MAP = get_genre_map()

def fetch_tmdb_movies():
    """Fetches popular movies from TMDb API to expand the dataset."""
    try:
        url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=en-US&page=1"
        response = requests.get(url)
        if response.status_code == 200:
            movies = response.json().get("results", [])
            new_movies = []
            for movie in movies:
                new_movies.append({
                    "title": movie.get("title", "Unknown"),
                    "overview": movie.get("overview", "No overview available."),
                    "genres": ", ".join([GENRE_MAP.get(genre_id, "Unknown") for genre_id in movie.get("genre_ids", [])]),
                    "release_date": movie.get("release_date", "Unknown")
                })
            return new_movies
        else:
            print(f"Error fetching TMDb movies: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error in fetching TMDb movies: {e}")
        return []

# Fetch additional movies from TMDb
new_movies = fetch_tmdb_movies()
new_movies_df = pd.DataFrame(new_movies)

# Combine with existing dataset
df = pd.concat([df, new_movies_df], ignore_index=True)

# Feature extraction: We'll combine title, overview, genres, and cast into a single content string
df["content"] = df["title"] + " " + df["overview"].fillna("") + " " + df["genres"].fillna("") + " " + df["cast"].fillna("")

# Initialize the vectorizer and compute the TF-IDF matrix
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["content"])

# Compute similarity matrix
similarity = cosine_similarity(tfidf_matrix)

# Save models
try:
    with open("models/movies.pkl", "wb") as f:
        pickle.dump(df, f)
    with open("models/similarity.pkl", "wb") as f:
        pickle.dump(similarity, f)
    print("✅ Similarity matrix updated successfully with TMDb data!")
except Exception as e:
    print(f"Error saving models: {e}")


