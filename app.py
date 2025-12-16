from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
import os
import pandas as pd
from recommender import MovieRecommender

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production-12345'

# Initialize recommender
print("Initializing Movie Recommender...")
recommender = MovieRecommender()
print("Recommender initialized successfully!")

# Available genres
AVAILABLE_GENRES = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Drama',
    'Family', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Sci-Fi',
    'Thriller', 'War', 'Western', 'Musical', 'Biography', 'Sport'
]

# Genre emoji mapping
GENRE_EMOJIS = {
    'Action': '💥', 'Adventure': '🗺️', 'Animation': '🎨', 'Comedy': '😂',
    'Crime': '🔫', 'Drama': '🎭', 'Family': '👨‍👩‍👧‍👦', 'Fantasy': '🧙',
    'Horror': '👻', 'Mystery': '🔍', 'Romance': '💕', 'Sci-Fi': '🚀',
    'Thriller': '😱', 'War': '⚔️', 'Western': '🤠', 'Musical': '🎵',
    'Biography': '📖', 'Sport': '⚽'
}


@app.route('/')
def index():
    """Landing page"""
    session.clear()
    return render_template('index.html')


@app.route('/step1', methods=['GET', 'POST'])
def step1_genres():
    """Step 1: Genre preference selection"""
    if request.method == 'POST':
        selected_genres = request.form.getlist('genres')
        
        if not selected_genres:
            return render_template('step1_genres.html', 
                                 genres=AVAILABLE_GENRES,
                                 genre_emojis=GENRE_EMOJIS,
                                 error="Please select at least one genre!")
        
        session['genres'] = selected_genres
        print(f"✓ User selected genres: {selected_genres}")
        return redirect(url_for('step2_ratings'))
    
    return render_template('step1_genres.html', 
                         genres=AVAILABLE_GENRES,
                         genre_emojis=GENRE_EMOJIS)


@app.route('/step2', methods=['GET', 'POST'])
def step2_ratings():
    """Step 2: Seed ratings collection"""
    if request.method == 'POST':
        seed_ratings = {}
        
        for key, value in request.form.items():
            if key.startswith('rating_') and value != 'not_watched':
                movie_id = int(key.split('_')[1])
                seed_ratings[movie_id] = int(value)
        
        if len(seed_ratings) < 3:
            movies = recommender.get_popular_movies_for_seeding(10)
            return render_template('step2_ratings.html', 
                                 movies=movies.to_dict('records'),
                                 error="Please rate at least 3 movies!")
        
        session['seed_ratings'] = seed_ratings
        print(f"✓ User rated {len(seed_ratings)} movies")
        return redirect(url_for('step3_context'))
    
    movies = recommender.get_popular_movies_for_seeding(10)
    return render_template('step2_ratings.html', 
                         movies=movies.to_dict('records'))


@app.route('/step3', methods=['GET', 'POST'])
def step3_context():
    """Step 3: Contextual filters"""
    if request.method == 'POST':
        session['mood'] = request.form.get('mood')
        session['occasion'] = request.form.get('occasion')
        session['time_budget'] = request.form.get('time_budget')
        
        print(f"✓ Context: {session['mood']}, {session['occasion']}, {session['time_budget']}")
        return redirect(url_for('results'))
    
    return render_template('step3_context.html')


@app.route('/results')
def results():
    """Display personalized recommendations"""
    user_input = {
        'genres': session.get('genres', []),
        'seed_ratings': session.get('seed_ratings', {}),
        'mood': session.get('mood', ''),
        'occasion': session.get('occasion', ''),
        'time_budget': session.get('time_budget', '')
    }
    
    if not user_input['genres'] or not user_input['seed_ratings']:
        return redirect(url_for('index'))
    
    print("\n" + "="*70)
    print("GENERATING RECOMMENDATIONS")
    print("="*70)
    print(f"Genres: {user_input['genres']}")
    print(f"Seed Ratings: {len(user_input['seed_ratings'])} movies rated")
    print(f"Mood: {user_input['mood']}")
    print(f"Occasion: {user_input['occasion']}")
    print(f"Time Budget: {user_input['time_budget']}")
    
    # Get recommendations
    recommendations = recommender.get_recommendations(user_input, n=10)
    
    print(f"✓ Generated {len(recommendations)} recommendations")
    
    # Fetch movie details from API (OMDb, TMDB, or None)
    movie_list = []
    for _, movie in recommendations.iterrows():
        movie_dict = movie.to_dict()
        
        # Use the unified fetch method (automatically picks OMDb/TMDB/None)
        api_details = recommender.fetch_movie_details(movie['title'])
        
        if api_details:
            movie_dict.update(api_details)
            print(f"  ✓ Fetched details for: {movie['title']}")
        else:
            # Use local data if API not available
            if 'overview' in movie_dict and pd.notna(movie_dict['overview']):
                print(f"  ℹ Using local data for: {movie['title']}")
            else:
                movie_dict['overview'] = 'No description available.'
                print(f"  ⚠ No details for: {movie['title']}")
        
        movie_list.append(movie_dict)
    
    print("="*70 + "\n")
    
    return render_template('results.html', 
                         movies=movie_list,
                         user_prefs=user_input)


@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """API endpoint for recommendations"""
    try:
        data = request.get_json()
        
        if 'seed_ratings' in data:
            data['seed_ratings'] = {int(k): v for k, v in data['seed_ratings'].items()}
        
        recommendations = recommender.get_recommendations(data, n=10)
        result = recommendations.to_dict('records')
        
        return jsonify({
            'success': True,
            'count': len(result),
            'recommendations': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/movies/popular')
def api_popular_movies():
    """API endpoint to get popular movies"""
    try:
        movies = recommender.get_popular_movies_for_seeding(10)
        return jsonify({
            'success': True,
            'movies': movies.to_dict('records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'movies_loaded': len(recommender.movies),
        'ratings_loaded': len(recommender.ratings),
        'api_configured': 'Yes' if hasattr(recommender, 'fetch_movie_details') else 'No'
    })


@app.errorhandler(404)
def not_found(e):
    return 'Page not found', 404


@app.errorhandler(500)
def server_error(e):
    return 'Internal server error', 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎬 MOVIE RECOMMENDATION SYSTEM")
    print("="*70)
    print(f"✓ Loaded {len(recommender.movies)} movies")
    print(f"✓ Loaded {len(recommender.ratings)} ratings")
    print(f"✓ Available genres: {len(AVAILABLE_GENRES)}")
    
    # Check which API is configured
    from recommender import USE_OMDB, USE_TMDB, USE_NO_API, OMDB_API_KEY, TMDB_API_KEY
    
    if USE_NO_API:
        print("ℹ️  API Mode: No API (Local data only)")
    elif USE_OMDB and OMDB_API_KEY != "YOUR_OMDB_KEY_HERE":
        print("✓ API Mode: OMDb API configured")
    elif USE_TMDB and TMDB_API_KEY != "YOUR_TMDB_KEY_HERE":
        print("✓ API Mode: TMDB API configured")
    else:
        print("⚠️  API Warning: No API key found (using local data)")
        print("   Get FREE OMDb key: http://www.omdbapi.com/apikey.aspx")
    
    print("\n🌐 Starting Flask server...")
    print("📍 Main App: http://localhost:5000")
    print("📍 API: http://localhost:5000/api/recommend")
    print("📍 Health: http://localhost:5000/health")
    print("\n💡 Quick Setup:")
    print("   1. Get FREE OMDb API key (takes 1 minute)")
    print("   2. Update OMDB_API_KEY in recommender.py")
    print("   3. Enjoy movie posters and descriptions!")
    print("="*70 + "\n")
    

    app.run(debug=True, host='0.0.0.0', port=5000)

