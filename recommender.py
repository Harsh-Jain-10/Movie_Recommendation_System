import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import requests

# Import from config
try:
    from config import (
        USE_OMDB, OMDB_API_KEY, USE_TMDB, TMDB_API_KEY, TMDB_BASE_URL,
        USE_NO_API, CONTENT_WEIGHT, COLLABORATIVE_WEIGHT
    )
except ImportError:
    # Fallback if config.py not found
    print("⚠️ config.py not found, using default settings")
    USE_OMDB = False
    OMDB_API_KEY = "YOUR_OMDB_KEY_HERE"
    USE_TMDB = False
    TMDB_API_KEY = "YOUR_TMDB_KEY_HERE"
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    USE_NO_API = True
    CONTENT_WEIGHT = 0.7
    COLLABORATIVE_WEIGHT = 0.3


class MovieRecommender:
    def __init__(self, movies_csv='data/movies_dataset.csv', ratings_csv='data/ratings_dataset.csv'):
        """Initialize the recommendation engine"""
        self.load_data(movies_csv, ratings_csv)
        self.prepare_content_features()
        self.prepare_collaborative_model()
        
    def load_data(self, movies_csv, ratings_csv):
        """Load movie and ratings datasets"""
        try:
            self.movies = pd.read_csv(movies_csv)
            self.ratings = pd.read_csv(ratings_csv)
            print(f"✓ Loaded {len(self.movies)} movies and {len(self.ratings)} ratings")
        except FileNotFoundError:
            print("⚠ Dataset not found. Creating dummy data...")
            self._create_dummy_data()
    
    def _create_dummy_data(self):
        """Create dummy dataset for demonstration"""
        self.movies = pd.DataFrame({
            'movieId': range(1, 51),
            'title': [
                'The Shawshank Redemption', 'The Godfather', 'The Dark Knight',
                'Inception', 'Pulp Fiction', 'Forrest Gump', 'The Matrix',
                'Goodfellas', 'Se7en', 'Interstellar', 'Titanic', 'Avatar',
                'The Avengers', 'Jurassic Park', 'Toy Story', 'Finding Nemo',
                'The Lion King', 'Frozen', 'Coco', 'Up', 'Die Hard',
                'Terminator 2', 'Aliens', 'Predator', 'RoboCop',
                'The Notebook', 'La La Land', 'Pride and Prejudice',
                'Casablanca', 'Roman Holiday', 'The Exorcist', 'The Shining',
                'A Quiet Place', 'Get Out', 'Hereditary', 'The Conjuring',
                'Superbad', 'The Hangover', 'Bridesmaids', 'Step Brothers',
                '3 Idiots', 'Dangal', 'PK', 'Lagaan', 'Dilwale Dulhania Le Jayenge',
                'Parasite', 'Oldboy', 'Spirited Away', 'Your Name', 'Train to Busan'
            ],
            'genres': [
                'Drama', 'Crime|Drama', 'Action|Crime|Drama', 'Action|Sci-Fi|Thriller',
                'Crime|Drama', 'Drama|Romance', 'Action|Sci-Fi', 'Crime|Drama',
                'Crime|Mystery|Thriller', 'Sci-Fi|Drama|Adventure', 'Drama|Romance',
                'Action|Adventure|Sci-Fi', 'Action|Adventure|Sci-Fi', 'Adventure|Sci-Fi|Thriller',
                'Animation|Adventure|Comedy', 'Animation|Adventure|Comedy', 'Animation|Adventure|Drama',
                'Animation|Adventure|Comedy|Family', 'Animation|Adventure|Comedy|Family',
                'Animation|Adventure|Comedy|Drama', 'Action|Thriller', 'Action|Sci-Fi|Thriller',
                'Action|Adventure|Sci-Fi|Thriller', 'Action|Adventure|Sci-Fi|Thriller',
                'Action|Crime|Sci-Fi|Thriller', 'Drama|Romance', 'Drama|Musical|Romance',
                'Drama|Romance', 'Drama|Romance', 'Drama|Romance', 'Horror|Mystery|Thriller',
                'Horror|Thriller', 'Drama|Horror|Mystery|Thriller', 'Horror|Mystery|Thriller',
                'Drama|Horror|Mystery|Thriller', 'Horror|Mystery|Thriller', 'Comedy',
                'Comedy', 'Comedy|Romance', 'Comedy', 'Comedy|Drama', 'Biography|Drama|Sport',
                'Comedy|Drama|Sci-Fi', 'Drama|Sport', 'Drama|Romance|Musical', 'Drama|Thriller',
                'Crime|Drama|Mystery|Thriller', 'Animation|Adventure|Fantasy', 'Animation|Drama|Romance',
                'Action|Horror|Thriller'
            ],
            'runtime': np.random.randint(80, 180, 50).tolist(),
            'rating': np.random.uniform(3.5, 5.0, 50).round(1).tolist(),
            'year': [1994, 1972, 2008, 2010, 1994, 1994, 1999, 1990, 1995, 2014, 
                    1997, 2009, 2012, 1993, 1995, 2003, 1994, 2013, 2017, 2009,
                    1988, 1991, 1986, 1987, 1987, 2004, 2016, 2005, 1942, 1953,
                    1973, 1980, 2018, 2017, 2018, 2013, 2007, 2009, 2011, 2008,
                    2009, 2016, 2014, 2001, 1995, 2019, 2003, 2001, 2016, 2016]
        })
        
        # Add overview/plot descriptions
        self.movies['overview'] = [
            'Two imprisoned men bond over years, finding redemption through acts of decency.',
            'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.',
            'When menace known as Joker emerges, Batman must accept one of greatest psychological tests.',
            'A thief who steals secrets through dreams is given a chance at redemption.',
            'Various interconnected people grapple with questions of life, death, and meaning.',
            'The presidencies of Kennedy and Johnson unfold through the perspective of an Alabama man.',
            'A computer hacker learns the true nature of his reality and his role in the war against controllers.',
            'The story of Henry Hill and his life in the mob, covering his relationship with his wife and partners.',
            'Two detectives hunt a serial killer who uses the seven deadly sins as his motives.',
            'A team of explorers travel through a wormhole in space in an attempt to ensure survival.',
            'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious ship.',
            'A paraplegic Marine dispatched to the moon Pandora on a unique mission.',
            'Earth\'s mightiest heroes must come together to stop an alien invasion.',
            'Scientists clone dinosaurs to populate a theme park which suffers a major security breakdown.',
            'A cowboy doll is profoundly threatened when a new spaceman figure supplants him.',
            'After his son is captured, a timid clownfish sets out on a journey to bring him home.',
            'Lion prince Simba flees his kingdom only to learn the true meaning of responsibility.',
            'When the newly crowned Queen Elsa accidentally uses her power to turn things into ice.',
            'A young boy embarks on a magical adventure to the Land of the Dead.',
            'Elderly widower Carl goes on an adventure in his flying house.',
            'An NYPD officer tries to save his wife and several others taken hostage during a Christmas party.',
            'The cyborg protector returns to prevent the death of future rebel leader John Connor.',
            'Colonists fight hostile alien life forms and an android with hidden agenda.',
            'A team of commandos is hunted by an extraterrestrial warrior in the jungle.',
            'In a dystopic crime-ridden Detroit, a terminally wounded cop returns to the force as a cyborg.',
            'A poor yet passionate young man falls in love with a rich young woman.',
            'A jazz pianist falls for an aspiring actress in Los Angeles.',
            'Sparks fly when spirited Elizabeth Bennet meets single, rich, and proud Mr. Darcy.',
            'A cynical American expatriate struggles to decide whether to help his former lover escape.',
            'A princess falls in love with a reporter during her tour of European capitals.',
            'When a young girl is possessed by a mysterious entity, her mother seeks help from two priests.',
            'A family heads to an isolated hotel where a sinister presence influences the father.',
            'A family is forced to live in silence while hiding from creatures that hunt by sound.',
            'A young African-American visits his white girlfriend\'s parents, uncovering a disturbing secret.',
            'A grieving family is haunted by tragic and disturbing occurrences.',
            'Paranormal investigators work to help a family terrorized by a dark presence.',
            'Two co-dependent high school seniors are forced to deal with separation anxiety.',
            'Three buddies wake up with no memory of the previous night and search for the missing groom.',
            'Competition between bridesmaids escalates to absurd heights.',
            'Two aimless middle-aged losers still living at home are forced to become roommates.',
            'Three friends embark on a quest to change one engineer\'s life before graduation.',
            'Former wrestler becomes a girls\' wrestling coach to fulfill his father\'s dream.',
            'An alien on Earth poses difficult questions about life and humanity.',
            'Villagers unite to challenge British officers at cricket, their only hope for freedom.',
            'Two lovers face disapproval and must elope to realize their dreams.',
            'Greed and class discrimination threaten the newly formed symbiotic relationship between families.',
            'After being kidnapped and imprisoned, a man seeks revenge on his captors.',
            'A young girl enters a world ruled by gods, witches, and spirits.',
            'Two teenagers share a profound connection after discovering they are swapping bodies.',
            'Passengers on a train must fight for survival against a zombie outbreak.'
        ]
        
        # Create dummy ratings
        np.random.seed(42)
        ratings_data = []
        for user in range(1, 101):
            n_ratings = np.random.randint(10, 30)
            movie_ids = np.random.choice(self.movies['movieId'], n_ratings, replace=False)
            for movie_id in movie_ids:
                rating = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.1, 0.2, 0.35, 0.3])
                ratings_data.append({'userId': user, 'movieId': int(movie_id), 'rating': float(rating)})
        
        self.ratings = pd.DataFrame(ratings_data)
    
    def prepare_content_features(self):
        """Prepare TF-IDF features for content-based filtering"""
        self.movies['genres_clean'] = self.movies['genres'].str.replace('|', ' ')
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies['genres_clean'])
    
    def prepare_collaborative_model(self):
        """Prepare user-item matrix for collaborative filtering"""
        self.user_item_matrix = self.ratings.pivot_table(
            index='userId',
            columns='movieId',
            values='rating'
        ).fillna(0)
        
        self.knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        self.knn_model.fit(self.user_item_matrix.T)
    
    def content_based_score(self, user_preferences):
        """Calculate content-based scores"""
        selected_genres = user_preferences.get('genres', [])
        mood = user_preferences.get('mood', '')
        
        mood_genre_map = {
            'Happy': ['Comedy', 'Adventure', 'Family', 'Musical'],
            'Sad': ['Drama', 'Romance'],
            'Adventurous': ['Action', 'Adventure', 'Sci-Fi', 'Thriller'],
            'Relaxed': ['Comedy', 'Animation', 'Romance', 'Family']
        }
        
        if mood in mood_genre_map:
            selected_genres = selected_genres + mood_genre_map[mood]
        
        user_profile = ' '.join(selected_genres)
        user_vector = self.tfidf.transform([user_profile])
        similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
        
        return pd.Series(similarities, index=self.movies['movieId'].values)
    
    def collaborative_score(self, seed_ratings):
        """Calculate collaborative filtering scores"""
        if not seed_ratings:
            return pd.Series(dtype=float)
        
        user_vector = pd.Series(0.0, index=self.user_item_matrix.columns)
        for movie_id, rating in seed_ratings.items():
            if movie_id in user_vector.index:
                user_vector[movie_id] = float(rating)
        
        scores = {}
        for movie_id in user_vector[user_vector > 0].index:
            if movie_id not in self.user_item_matrix.columns:
                continue
                
            movie_idx = list(self.user_item_matrix.columns).index(movie_id)
            
            try:
                distances, indices = self.knn_model.kneighbors(
                    self.user_item_matrix.T.iloc[movie_idx].values.reshape(1, -1),
                    n_neighbors=min(11, len(self.user_item_matrix.columns))
                )
                
                for i, idx in enumerate(indices.flatten()[1:]):
                    similar_movie_id = self.user_item_matrix.columns[idx]
                    if similar_movie_id not in seed_ratings:
                        similarity = 1 - distances.flatten()[i+1]
                        scores[similar_movie_id] = scores.get(similar_movie_id, 0.0) + (
                            similarity * user_vector[movie_id]
                        )
            except Exception as e:
                print(f"Warning: Error in collaborative filtering for movie {movie_id}: {e}")
                continue
        
        return pd.Series(scores, dtype=float)
    
    def apply_contextual_filters(self, recommendations, context):
        """Apply contextual filters"""
        filtered = recommendations.copy()
        
        occasion = context.get('occasion', '')
        if occasion == 'Family':
            filtered = filtered[~filtered['genres'].str.contains('Horror|Crime|Thriller', na=False, case=False)]
        
        time_budget = context.get('time_budget', 'No limit')
        if time_budget == '< 90 mins':
            filtered = filtered[filtered['runtime'] < 90]
        elif time_budget == '< 2 hours':
            filtered = filtered[filtered['runtime'] < 120]
        
        return filtered
    
    def get_recommendations(self, user_input, n=10):
        """
        Main recommendation function - FIXED VERSION
        """
        try:
            # Content-based scores
            content_scores = self.content_based_score({
                'genres': user_input.get('genres', []),
                'mood': user_input.get('mood', '')
            })
            
            # Collaborative scores
            collab_scores = self.collaborative_score(user_input.get('seed_ratings', {}))
            
            # Normalize scores
            if len(content_scores) > 0 and content_scores.sum() > 0:
                content_scores = content_scores / content_scores.max()
            else:
                content_scores = pd.Series(0.0, index=self.movies['movieId'].values)
            
            if len(collab_scores) > 0 and collab_scores.sum() > 0:
                collab_scores = collab_scores / collab_scores.max()
            else:
                collab_scores = pd.Series(0.0, index=self.movies['movieId'].values)
            
            # Combine scores (weighted hybrid)
            combined_scores = (
                CONTENT_WEIGHT * content_scores +
                COLLABORATIVE_WEIGHT * collab_scores.reindex(content_scores.index, fill_value=0.0)
            )
            
            # CRITICAL FIX: Ensure all values are numeric
            combined_scores = pd.to_numeric(combined_scores, errors='coerce').fillna(0.0)
            
            # Remove already rated movies
            rated_movies = set(user_input.get('seed_ratings', {}).keys())
            combined_scores = combined_scores[~combined_scores.index.isin(rated_movies)]
            
            # Check if we have any valid scores
            if len(combined_scores) == 0 or combined_scores.sum() == 0:
                print("⚠️ No scores generated, returning popular movies as fallback")
                return self.get_popular_movies_for_seeding(n)
            
            # Get top movies - ensure we don't request more than available
            n_movies = min(n * 3, len(combined_scores))
            top_movie_ids = combined_scores.nlargest(n_movies).index
            
            recommendations = self.movies[self.movies['movieId'].isin(top_movie_ids)].copy()
            recommendations['score'] = recommendations['movieId'].map(combined_scores).fillna(0.0)
            recommendations = recommendations.sort_values('score', ascending=False)
            
            # Apply contextual filters
            recommendations = self.apply_contextual_filters(
                recommendations,
                {
                    'occasion': user_input.get('occasion', ''),
                    'time_budget': user_input.get('time_budget', '')
                }
            )
            
            # Ensure we have recommendations after filtering
            if len(recommendations) == 0:
                print("⚠️ No recommendations after filtering, returning popular movies")
                return self.get_popular_movies_for_seeding(n)
            
            return recommendations.head(n)
        
        except Exception as e:
            print(f"❌ Error in get_recommendations: {e}")
            import traceback
            traceback.print_exc()
            print("📊 Falling back to popular movies")
            return self.get_popular_movies_for_seeding(n)
    
    def get_popular_movies_for_seeding(self, n=10):
        """Get popular movies for seed rating step"""
        movie_stats = self.ratings.groupby('movieId').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        movie_stats.columns = ['movieId', 'avg_rating', 'count']
        movie_stats = movie_stats[movie_stats['count'] >= 5]
        movie_stats['popularity'] = movie_stats['avg_rating'] * np.log(movie_stats['count'] + 1)
        
        top_movies = movie_stats.nlargest(min(n, len(movie_stats)), 'popularity')
        result = self.movies[self.movies['movieId'].isin(top_movies['movieId'])]
        return result.head(n)
    
    def fetch_movie_details(self, movie_title):
        """Fetch movie details using configured API"""
        if USE_NO_API:
            return None
        
        if USE_OMDB and OMDB_API_KEY != "YOUR_OMDB_KEY_HERE":
            return self.fetch_omdb_details(movie_title)
        
        if USE_TMDB and TMDB_API_KEY != "YOUR_TMDB_KEY_HERE":
            return self.fetch_tmdb_details(movie_title)
        
        return None
    
    def fetch_omdb_details(self, movie_title):
        """Fetch movie details from OMDb API"""
        try:
            clean_title = movie_title.split('(')[0].strip()
            url = "http://www.omdbapi.com/"
            params = {
                'apikey': OMDB_API_KEY,
                't': clean_title,
                'type': 'movie',
                'plot': 'short'
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    return {
                        'poster_url': data.get('Poster', '') if data.get('Poster') != 'N/A' else None,
                        'overview': data.get('Plot', 'No description available.'),
                        'release_date': data.get('Released', ''),
                        'vote_average': float(data.get('imdbRating', 0)) if data.get('imdbRating', 'N/A') != 'N/A' else 0,
                        'director': data.get('Director', ''),
                        'actors': data.get('Actors', ''),
                        'imdb_rating': data.get('imdbRating', 'N/A')
                    }
        except Exception as e:
            print(f"OMDb API Error for '{movie_title}': {e}")
        
        return None
    
    def fetch_tmdb_details(self, movie_title):
        """Fetch movie details from TMDB API"""
        try:
            search_url = f"{TMDB_BASE_URL}/search/movie"
            params = {'api_key': TMDB_API_KEY, 'query': movie_title}
            response = requests.get(search_url, params=params, timeout=5)
            
            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    movie = results[0]
                    return {
                        'poster_url': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}" if movie.get('poster_path') else None,
                        'overview': movie.get('overview', 'No description available.'),
                        'release_date': movie.get('release_date', ''),
                        'vote_average': movie.get('vote_average', 0)
                    }
        except Exception as e:
            print(f"TMDB API Error for '{movie_title}': {e}")
        

        return None
