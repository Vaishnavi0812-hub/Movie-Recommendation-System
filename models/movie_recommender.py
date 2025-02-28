import pandas as pd
import pickle
import requests

import requests

# TMDb API Key
API_KEY = "e588fc141b95bf18111a19119c28c21b"
BASE_URL = "https://api.themoviedb.org/3"

def get_movie_id_from_tmdb(movie_name):
    """Fetch the movie ID from TMDb API based on the given movie name."""
    search_url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": movie_name}
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]["id"]  # Return the first movie ID
    return None

def fetch_recommendations_from_tmdb(movie_id):
    """Fetch recommended movies from TMDb based on the movie ID."""
    url = f"{BASE_URL}/movie/{movie_id}/recommendations"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        recommendations = []
        for movie in data["results"][:5]:  # Get top 5 recommended movies
            recommendations.append({
                "title": movie["title"],
                "overview": movie["overview"],
                "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie["poster_path"] else "static/default_poster.jpg"
            })
        return recommendations
    return []

def recommend(movie_name):
    """Fetch movie recommendations based on the movie name."""
    movie_id = get_movie_id_from_tmdb(movie_name)
    
    if not movie_id:
        print(f"⚠️ Movie '{movie_name}' not found on TMDb.")
        return []

    recommendations = fetch_recommendations_from_tmdb(movie_id)
    return recommendations
 
