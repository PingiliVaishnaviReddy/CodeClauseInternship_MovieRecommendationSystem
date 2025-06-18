from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset
movies = pd.read_csv("TeluguMovies_dataset.csv")
movies['Genre'] = movies['Genre'].fillna('')
movies['Rating'] = movies['Rating'].fillna(0)

def recommend_movies(user_genres, user_rating, top_n=10):
    filtered = movies[
        movies['Genre'].apply(lambda x: any(genre in x for genre in user_genres)) &
        (movies['Rating'] >= user_rating)
    ]
    filtered = filtered.sort_values(by='Rating', ascending=False).head(top_n)

    return [
        {
            'Movie': row['Movie'],
            'Genre': row['Genre'],
            'Rating': row['Rating'],
            'Runtime': row['Runtime']
        }
        for _, row in filtered.iterrows()
    ]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        genres = request.form.getlist('genre')
        rating = float(request.form['rating'])
        recommended_movies = recommend_movies(genres, rating)
        return render_template('index.html', recommended_movies=recommended_movies)
    return render_template('index.html', recommended_movies=None)

if __name__ == '__main__':
    app.run(debug=True)
