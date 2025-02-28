import requests

# Replace with your actual API key
TMDB_API_KEY = "e588fc141b95bf18111a19119c28c21b"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def fetch_movie_details(movie_title):
    """
    Fetch movie details from TMDb API based on the given movie title.
    """
    search_url = f"{TMDB_BASE_URL}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": movie_title}
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Will raise an HTTPError if the response code is 4xx/5xx

        data = response.json()
        if data["results"]:
            movie = data["results"][0]  # Get the first movie result
            return {
                "title": movie.get("title", "Unknown"),
                "overview": movie.get("overview", "No overview available."),
                "poster_path": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else "static/default_poster.jpg"
            }
        else:
            return {
                "title": movie_title,
                "overview": "No overview available.",
                "poster_path": "static/default_poster.jpg"
            }
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie details: {e}")
        return {
            "title": movie_title,
            "overview": "No details found.",
            "poster_path": "static/default_poster.jpg"
        }

# Test the function
if __name__ == "__main__":
    movie_name = "Inception"  # Example movie
    details = fetch_movie_details(movie_name)
    print(details)
