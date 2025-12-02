# config.py
"""
Configuration file for API keys and settings
"""

# TMDB API Configuration
# Get your API key from: https://www.themoviedb.org/settings/api
TMDB_API_KEY = "YOUR_TMDB_API_KEY_HERE"  # Replace with your actual key
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Application Settings
SECRET_KEY = "your-secret-key-change-in-production"
DEBUG = True

# Recommendation Engine Parameters
CONTENT_WEIGHT = 0.7  # 70% content-based
COLLABORATIVE_WEIGHT = 0.3  # 30% collaborative
MIN_SEED_RATINGS = 3  # Minimum ratings required from user