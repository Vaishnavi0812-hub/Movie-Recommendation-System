from flask import Flask, render_template, request, jsonify
import requests

API_KEY = "e588fc141b95bf18111a19119c28c21b"
BASE_URL = "https://api.themoviedb.org/3"

# Define recommend function
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
        print("TMDb recommendations response:", data)  # Debug print
        recommendations = []
        for movie in data["results"][:5]:  # Get top 5 recommended movies
            recommendations.append({
                "title": movie["title"],
                "overview": movie["overview"],
                "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie["poster_path"] else "static/default_poster.jpg"
            })
        return recommendations
    else:
        print(f"Failed to fetch recommendations: {response.status_code}")  # Debug print
    return []

def recommend(movie_name):
    """Fetch movie recommendations based on the movie name."""
    movie_id = get_movie_id_from_tmdb(movie_name)
    
    if not movie_id:
        print(f"⚠️ Movie '{movie_name}' not found on TMDb.")
        return []

    recommendations = fetch_recommendations_from_tmdb(movie_id)
    
    if not recommendations:
        print(f"⚠️ No recommendations found for movie: {movie_name}")
    
    return recommendations


# Flask setup
app = Flask(__name__)

@app.route('/')
def home():
    movie_name = "Inception"  # You can replace this with any movie name you want
    recommended_movies = recommend(movie_name)  # Use the 'recommend' function to get recommendations

    # Pass the recommended movies to the template
    return render_template('index.html', movies=recommended_movies)

@app.route("/recommend", methods=["POST"])
def recommend_movies():  
    data = request.json
    movie_name = data.get("movie_name", "").strip()

    if not movie_name:
        return jsonify({"error": "Movie name not provided"}), 400

    try:
        recommendations = recommend(movie_name)  # This should now work
        print(f"Recommendations for {movie_name}: {recommendations}")  # Debug print

        if not recommendations:
            return jsonify({"error": "No recommendations found."}), 404

        return jsonify({"recommendations": recommendations})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


