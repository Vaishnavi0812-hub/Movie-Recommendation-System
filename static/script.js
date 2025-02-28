document.getElementById("recommendButton").addEventListener("click", function () {
    let movieName = document.getElementById("movieInput").value.trim();
    
    if (movieName === "") {
        alert("Please enter a movie name.");
        return;
    }

    // Disable the button while fetching recommendations to prevent multiple clicks
    let recommendButton = document.getElementById("recommendButton");
    recommendButton.disabled = true;
    recommendButton.innerHTML = "Loading...";

    fetch("/recommend", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ movie_name: movieName })
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById("movieList");
        resultDiv.innerHTML = "";  // Clear previous results

        // Check for errors in the data response
        if (data.error) {
            resultDiv.innerHTML = `<p>${data.error}</p>`;
        } else {
            // Loop through the movie recommendations
            data.recommendations.forEach(movie => {
                let movieCard = `
                    <div class="movie-card">
                        <img src="${movie.poster_path}" alt="${movie.title}">
                        <h3>${movie.title}</h3>
                        <p>${movie.overview}</p>
                    </div>
                `;
                resultDiv.innerHTML += movieCard;
            });
        }

        // Re-enable the button after recommendations are displayed
        recommendButton.disabled = false;
        recommendButton.innerHTML = "Get Recommendations";
    })
    .catch(error => {
        console.error("Error fetching recommendations:", error);
        alert("An error occurred while fetching the recommendations.");
        
        // Re-enable the button in case of an error
        recommendButton.disabled = false;
        recommendButton.innerHTML = "Get Recommendations";
    });
});
