from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)
movies = pd.read_csv('data/TeluguMovies_dataset.csv')
movies['Genre'] = movies['Genre'].fillna('') 
movies['Rating'] = movies['Rating'].fillna(0)  
def recommend_movies(user_genres, user_rating, top_n=10):
    filtered_movies = movies[movies['Genre'].apply(lambda x: any(genre in x for genre in user_genres)) & (movies['Rating'] >= user_rating)]
    
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
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_genres = request.form.getlist('genre')
        user_rating = float(request.form['rating'])
        recommended_movies = recommend_movies(user_genres, user_rating)
        return render_template('index.html', recommended_movies=recommended_movies, user_genres=user_genres, user_rating=user_rating)
    return render_template('index.html', recommended_movies=None)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
