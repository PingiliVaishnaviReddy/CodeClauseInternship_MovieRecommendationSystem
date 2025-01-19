from flask import Flask, render_template, request
import pandas as pd

# Create the Flask app
app = Flask(__name__)

# Load the movie dataset
movies = pd.read_csv('data/TeluguMovies_dataset.csv')

# Preprocess the movie data
movies['Genre'] = movies['Genre'].fillna('')  # Handle missing genre values
movies['Rating'] = movies['Rating'].fillna(0)  # Handle missing ratings values

# Function to recommend movies based on selected genres and rating
def recommend_movies(user_genres, user_rating, top_n=10):
    # Filter movies based on selected genres and rating
    filtered_movies = movies[movies['Genre'].apply(lambda x: any(genre in x for genre in user_genres)) & (movies['Rating'] >= user_rating)]
    
    # Sort movies by rating in descending order and get top N
    filtered_movies = filtered_movies.sort_values(by='Rating', ascending=False).head(top_n)
    
    recommended_movies = []
    for _, row in filtered_movies.iterrows():
        recommended_movies.append({
            'Movie': row['Movie'],
            'Genre': row['Genre'],
            'Rating': row['Rating'],
            'Runtime': row['Runtime']
        })
    
    return recommended_movies

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the selected genres and rating from the form
        user_genres = request.form.getlist('genre')
        user_rating = float(request.form['rating'])
        
        # Get movie recommendations
        recommended_movies = recommend_movies(user_genres, user_rating)
        
        return render_template('index.html', recommended_movies=recommended_movies, user_genres=user_genres, user_rating=user_rating)
    
    return render_template('index.html', recommended_movies=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

