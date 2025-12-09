"""
Configuration settings for the Movie Recommendation System.
"""

import os

# ==========================
# 1. API CONFIGURATION
# ==========================

# OPTION 1: OMDb API (Enabled)
# Get key from: http://www.omdbapi.com/apikey.aspx
USE_OMDB = True
OMDB_API_KEY = "YOUR_OMDB_KEY_HERE"  # <--- PASTE YOUR KEY HERE
OMDB_BASE_URL = "http://www.omdbapi.com/"

# OPTION 2: TMDB API (Disabled)
USE_TMDB = False
TMDB_API_KEY = "YOUR_TMDB_KEY_HERE"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# OPTION 3: Offline Mode (No posters)
USE_NO_API = False

# ==========================
# 2. FLASK SETTINGS
# ==========================
SECRET_KEY = "dev-secret-key-change-this-in-production"
DEBUG = True
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

# ==========================
# 3. RECOMMENDER ENGINE
# ==========================
# Hybrid Weights (Must sum to 1.0)
CONTENT_WEIGHT = 0.7       # 70% based on Genres/Mood
COLLABORATIVE_WEIGHT = 0.3 # 30% based on User Ratings

# Logic Constraints
MIN_SEED_RATINGS = 3       # User must rate 3 movies
MIN_GENRE_SELECTION = 1    # User must pick 1 genre
DEFAULT_RECOMMENDATION_COUNT = 10

# ==========================
# 4. DATA CONFIGURATION
# ==========================
MOVIES_DATASET_PATH = "data/movies_dataset.csv"
RATINGS_DATASET_PATH = "data/ratings_dataset.csv"

# Dummy Data Generator (Used if CSVs are missing)
AUTO_CREATE_DUMMY_DATA = True
DUMMY_MOVIES_COUNT = 50
DUMMY_USERS_COUNT = 100

# ==========================
# 5. ADVANCED FEATURES
# ==========================
ENABLE_API_ENDPOINTS = True # Allows /api/recommend for external apps

