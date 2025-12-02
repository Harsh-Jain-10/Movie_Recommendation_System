# 🎬 Movie Recommendation System

A sophisticated hybrid movie recommendation web application that solves the **cold start problem** through intelligent multi-step user onboarding.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### Core Functionality
- ✅ **Multi-Step Onboarding** - Comprehensive user preference collection
- ✅ **Hybrid Recommendation Engine** - 70% Content-Based + 30% Collaborative Filtering
- ✅ **Contextual Filtering** - Smart recommendations based on mood, occasion, and time
- ✅ **Cold Start Solution** - Works perfectly for new users with no history
- ✅ **RESTful API** - Voice interface ready with JSON endpoints
- ✅ **Responsive Design** - Works seamlessly on desktop, tablet, and mobile

### API Support
- ✅ **OMDb API Integration** - Movie posters, IMDb ratings, plot descriptions (FREE)
- ✅ **TMDB API Support** - Alternative API with larger database
- ✅ **Offline Mode** - Works without any API (local data only)

### User Experience
- ✅ **Beautiful UI** - Modern gradient design with smooth animations
- ✅ **Progressive Steps** - Three simple steps to get recommendations
- ✅ **Visual Feedback** - Real-time validation and progress indicators
- ✅ **Smart Filtering** - Automatic content filtering (e.g., no horror for family viewing)

---

## 📁 Project Structure

```
movie_recommender/
│
├── README.md                   # This file
├── config.py                   # Configuration and API keys
├── app.py                      # Flask application (main entry point)
├── recommender.py              # Recommendation engine logic
├── requirements.txt            # Python dependencies
│
├── data/
│   ├── movies_dataset.csv     # Movie database (auto-generated or MovieLens)
│   └── ratings_dataset.csv    # User ratings (auto-generated or MovieLens)
│
├── templates/
│   ├── index.html             # Landing page
│   ├── step1_genres.html      # Step 1: Genre selection
│   ├── step2_ratings.html     # Step 2: Seed ratings
│   ├── step3_context.html     # Step 3: Contextual filters
│   └── results.html           # Recommendations display
│
└── static/
    └── css/
        └── style.css          # All styling and animations
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for API features)

### Installation

#### 1. Clone/Download Project

```bash
# Create project directory
mkdir movie_recommender
cd movie_recommender

# Download all project files to this directory
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
flask==3.0.0
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
requests==2.31.0
```

#### 3. Configure API (Choose One Option)

**Option A: OMDb API (Recommended - Takes 1 Minute!)**

1. Visit: http://www.omdbapi.com/apikey.aspx
2. Select "FREE" plan (1,000 requests/day)
3. Enter your email
4. Check email for API key
5. Open `config.py` and update:
   ```python
   USE_OMDB = True
   OMDB_API_KEY = "your_key_here"  # Paste your key
   ```

**Option B: TMDB API (More Work)**

1. Visit: https://www.themoviedb.org/settings/api
2. Create account and request API key
3. Open `config.py` and update:
   ```python
   USE_OMDB = False
   USE_TMDB = True
   TMDB_API_KEY = "your_key_here"
   ```

**Option C: No API (Works Immediately)**

1. Open `config.py` and set:
   ```python
   USE_NO_API = True
   ```
2. App works perfectly, just no movie posters

#### 4. Run Application

```bash
python app.py
```

#### 5. Open in Browser

Navigate to: **http://localhost:5000**

---

## 📖 How to Use

### Step 1: Select Your Favorite Genres
- Choose any number of genres you enjoy
- Examples: Action, Comedy, Drama, Sci-Fi, Romance
- The more you select, the better the recommendations

### Step 2: Rate Popular Movies
- Rate at least 3 movies from the provided list (1-5 stars)
- Select "Haven't Watched" if you haven't seen a movie
- Your ratings help find users with similar taste

### Step 3: Set Your Context
- **Mood**: Happy, Sad, Adventurous, or Relaxed
- **Occasion**: Solo, Date, Family, or Friends
- **Time Budget**: < 90 mins, < 2 hours, or No limit

### Get Recommendations!
- View your personalized movie recommendations
- See match percentages, posters, and descriptions
- Save or print your recommendation list

---

## 🎯 The Recommendation Algorithm

### Hybrid Approach

The system uses a **weighted hybrid algorithm** that combines two methods:

#### 1. Content-Based Filtering (70%)
- Analyzes movie genres and attributes
- Uses TF-IDF vectorization
- Calculates cosine similarity between user preferences and movies
- Maps moods to relevant genres:
  - **Happy** → Comedy, Adventure, Family, Musical
  - **Sad** → Drama, Romance
  - **Adventurous** → Action, Adventure, Sci-Fi, Thriller
  - **Relaxed** → Comedy, Animation, Romance, Family

#### 2. Collaborative Filtering (30%)
- Analyzes user rating patterns
- Uses K-Nearest Neighbors algorithm
- Finds similar users based on seed ratings
- Recommends movies liked by similar users

### Contextual Filtering

After hybrid scoring, the system applies smart filters:

- **Occasion-Based**:
  - Family → Filters out Horror, Crime, mature content
  - Date → Prioritizes Romance, Drama
  - Friends → Includes Comedy, Action
  - Solo → No restrictions

- **Time-Based**:
  - < 90 mins → Shows only shorter films
  - < 2 hours → Excludes lengthy epics
  - No limit → All movies included

### Final Score Calculation

```
Final Score = (0.7 × Content Score) + (0.3 × Collaborative Score)
```

You can adjust these weights in `config.py`:
```python
CONTENT_WEIGHT = 0.7
COLLABORATIVE_WEIGHT = 0.3
```

---

## 🔌 API Documentation

### REST Endpoints

#### POST /api/recommend

Get movie recommendations via API (perfect for voice interfaces).

**Request:**
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "genres": ["Action", "Sci-Fi"],
    "seed_ratings": {"1": 5, "2": 4, "3": 3},
    "mood": "Adventurous",
    "occasion": "Solo",
    "time_budget": "< 2 hours"
  }'
```

**Response:**
```json
{
  "success": true,
  "count": 10,
  "recommendations": [
    {
      "movieId": 123,
      "title": "Inception",
      "genres": "Action|Sci-Fi|Thriller",
      "runtime": 148,
      "rating": 5.0,
      "score": 0.95,
      "overview": "A thief who steals secrets through dreams...",
      "poster_url": "https://..."
    }
  ]
}
```

**Python Example:**
```python
import requests

response = requests.post('http://localhost:5000/api/recommend', json={
    'genres': ['Action', 'Sci-Fi'],
    'seed_ratings': {1: 5, 2: 4, 3: 3},
    'mood': 'Adventurous',
    'occasion': 'Solo',
    'time_budget': '< 2 hours'
})

movies = response.json()['recommendations']
for movie in movies:
    print(f"{movie['title']} - {movie['score']:.0%} match")
```

#### GET /api/movies/popular

Get popular movies for seed rating.

**Response:**
```json
{
  "success": true,
  "movies": [
    {
      "movieId": 1,
      "title": "The Shawshank Redemption",
      "genres": "Drama",
      "runtime": 142
    }
  ]
}
```

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "movies_loaded": 9742,
  "ratings_loaded": 100836,
  "api_configured": "Yes"
}
```

---

## 📊 Dataset Options

### Option 1: Dummy Data (Default)

The system automatically creates 50 sample movies with synthetic ratings:

✅ **Pros:**
- Works immediately out of the box
- No download required
- Good for testing and demonstrations

❌ **Cons:**
- Limited movie selection (50 movies)
- Recommendations less accurate
- Smaller user base (100 synthetic users)

### Option 2: MovieLens Dataset (Recommended for Production)

Download real movie data with thousands of movies and ratings:

#### Small Dataset (100K ratings, ~9K movies)
1. Download from: https://grouplens.org/datasets/movielens/
2. Get `ml-latest-small.zip`
3. Extract files:
   ```bash
   unzip ml-latest-small.zip
   cp ml-latest-small/movies.csv data/movies_dataset.csv
   cp ml-latest-small/ratings.csv data/ratings_dataset.csv
   ```

#### Large Dataset (27M ratings, ~58K movies)
1. Download `ml-latest.zip` from same link
2. Extract and copy as above
3. Note: Initial load may take 30-60 seconds

✅ **Pros:**
- Huge movie database
- Real user ratings
- Highly accurate recommendations
- Production-ready quality

❌ **Cons:**
- Requires download (~1MB for small, ~265MB for large)
- Initial setup needed

### Dataset Format Requirements

#### movies_dataset.csv
```csv
movieId,title,genres
1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
2,Jumanji (1995),Adventure|Children|Fantasy
```

**Required Columns:**
- `movieId` - Unique integer ID
- `title` - Movie title (string)
- `genres` - Pipe-separated genres (e.g., "Action|Sci-Fi")

**Optional Columns:**
- `runtime` - Duration in minutes (integer)
- `year` - Release year (integer)
- `overview` - Plot description (string)

#### ratings_dataset.csv
```csv
userId,movieId,rating
1,1,4.0
1,3,4.0
```

**Required Columns:**
- `userId` - User ID (integer)
- `movieId` - Movie ID (integer)
- `rating` - Rating value (float, typically 1-5)

---

## ⚙️ Configuration

### config.py Settings

#### API Configuration
```python
# Choose one API option
USE_OMDB = True          # Easiest - free, instant
USE_TMDB = False         # More data, harder to get
USE_NO_API = False       # Works offline

# API Keys
OMDB_API_KEY = "your_key"
TMDB_API_KEY = "your_key"
```

#### Algorithm Tuning
```python
# Recommendation weights (must sum to 1.0)
CONTENT_WEIGHT = 0.7        # Genre matching
COLLABORATIVE_WEIGHT = 0.3  # User similarity

# Minimum requirements
MIN_SEED_RATINGS = 3        # Min movies to rate
MIN_GENRE_SELECTION = 1     # Min genres to select

# Recommendation count
DEFAULT_RECOMMENDATION_COUNT = 10
MAX_RECOMMENDATION_COUNT = 20
```

#### Server Settings
```python
SECRET_KEY = "change-in-production"
DEBUG = True                # Set False for production
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
```

---

## 🎨 Customization

### Change Color Scheme

Edit `static/css/style.css`:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your colors */
background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
```

### Add Custom Moods

Edit `recommender.py` in the `content_based_score()` method:

```python
mood_genre_map = {
    'Happy': ['Comedy', 'Adventure', 'Family'],
    'Sad': ['Drama', 'Romance'],
    'Adventurous': ['Action', 'Adventure', 'Sci-Fi'],
    'Relaxed': ['Comedy', 'Animation'],
    'Focused': ['Documentary', 'Biography'],  # Add new mood
    'Scary': ['Horror', 'Thriller']            # Add new mood
}
```

Then update `templates/step3_context.html` to include new options.

### Adjust Recommendation Count

In `app.py`, change the `results()` function:

```python
recommendations = recommender.get_recommendations(user_input, n=15)  # Default is 10
```

### Add New Genres

Edit `app.py`:

```python
AVAILABLE_GENRES = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Drama',
    'Family', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Sci-Fi',
    'Thriller', 'War', 'Western', 'Musical', 'Biography', 'Sport',
    'Documentary', 'Film-Noir', 'History'  # Add new genres
]
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: "Module not found"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

#### Issue: "No module named 'config'"
```bash
# Solution: Ensure config.py exists in the same directory as app.py
ls -la config.py
```

#### Issue: "Template not found"
```bash
# Solution: Check templates folder structure
ls templates/
# Should show: index.html, step1_genres.html, step2_ratings.html, etc.
```

#### Issue: "No movie posters showing"
```bash
# Solution: Check API configuration
# 1. Verify API key is correct in config.py
# 2. Check USE_OMDB = True or USE_TMDB = True
# 3. Test API key:
```

```python
import requests
response = requests.get(
    "http://www.omdbapi.com/",
    params={'apikey': 'YOUR_KEY', 't': 'Inception'}
)
print(response.json())
```

#### Issue: "Port 5000 already in use"
```python
# Solution: Change port in config.py
FLASK_PORT = 8080  # Or any other available port
```

#### Issue: "Recommendations seem random"
```bash
# Solutions:
# 1. Use MovieLens dataset instead of dummy data
# 2. Rate more movies (5+ instead of minimum 3)
# 3. Be more specific with genre selections
# 4. Check algorithm weights in config.py
```

#### Issue: "API limit exceeded"
```bash
# OMDb free tier: 1,000 requests/day
# Solution: Wait 24 hours or set USE_NO_API = True temporarily
```

### Debug Mode

Enable detailed logging in `config.py`:

```python
DEBUG = True
ENABLE_LOGGING = True
LOG_LEVEL = "DEBUG"
```

Then check console output when running:
```bash
python app.py
```

---

## 🚀 Deployment

### Production Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in config.py to a random string
- [ ] Set `DEBUG = False` in config.py
- [ ] Use real dataset (MovieLens) instead of dummy data
- [ ] Configure proper API keys
- [ ] Set up HTTPS/SSL
- [ ] Enable rate limiting
- [ ] Set up logging to files
- [ ] Configure database for user persistence (optional)
- [ ] Test all endpoints thoroughly

### Deploy to Heroku

```bash
# 1. Create Procfile
echo "web: python app.py" > Procfile

# 2. Create runtime.txt
echo "python-3.10.0" > runtime.txt

# 3. Initialize git
git init
git add .
git commit -m "Initial commit"

# 4. Create Heroku app
heroku create your-app-name

# 5. Deploy
git push heroku main
```

### Deploy to Docker

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t movie-recommender .
docker run -p 5000:5000 movie-recommender
```

---

## 📈 Performance Optimization

### For Large Datasets

If using MovieLens large dataset (27M ratings):

1. **Enable Caching** (future feature):
   ```python
   ENABLE_CACHING = True
   ```

2. **Limit Rating History**:
   ```python
   # In recommender.py, limit loaded ratings
   self.ratings = self.ratings.sample(n=1000000)  # Sample 1M ratings
   ```

3. **Use Sparse Matrices**:
   Already implemented in the collaborative filtering algorithm.

### API Rate Limiting

To avoid hitting API limits:

```python
# In config.py
ENABLE_RATE_LIMITING = True
RATE_LIMIT_PER_MINUTE = 60
```

---

## 🧪 Testing

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test API endpoint
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"genres": ["Action"], "seed_ratings": {"1": 5, "2": 4, "3": 3}, "mood": "Happy", "occasion": "Solo", "time_budget": "No limit"}'
```

### Unit Tests (Future Enhancement)

Create `tests/test_recommender.py`:

```python
import unittest
from recommender import MovieRecommender

class TestRecommender(unittest.TestCase):
    def setUp(self):
        self.recommender = MovieRecommender()
    
    def test_recommendations(self):
        user_input = {
            'genres': ['Action', 'Sci-Fi'],
            'seed_ratings': {1: 5, 2: 4, 3: 3},
            'mood': 'Adventurous',
            'occasion': 'Solo',
            'time_budget': 'No limit'
        }
        recommendations = self.recommender.get_recommendations(user_input, n=10)
        self.assertEqual(len(recommendations), 10)

if __name__ == '__main__':
    unittest.main()
```

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

### High Priority
- [ ] User authentication and profile persistence
- [ ] Save favorite movies and recommendation history
- [ ] Social features (share recommendations)
- [ ] More API integrations (Netflix, Amazon Prime availability)

### Medium Priority
- [ ] Advanced filtering (year, director, actors)
- [ ] Multi-language support (Bollywood, Korean, etc.)
- [ ] Deep learning embeddings for better recommendations
- [ ] A/B testing framework for algorithm improvements

### Low Priority
- [ ] Dark mode toggle
- [ ] Export recommendations to PDF
- [ ] Email recommendations
- [ ] Integration with calendar apps

### How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Create a Pull Request

---

## 📚 Tech Stack

### Backend
- **Flask 3.0.0** - Web framework
- **Pandas 2.1.4** - Data manipulation
- **NumPy 1.26.2** - Numerical computing
- **Scikit-learn 1.3.2** - Machine learning algorithms
- **Requests 2.31.0** - HTTP library for API calls

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with gradients and animations
- **JavaScript** - Form validation and interactivity
- **Responsive Design** - Works on all devices

### APIs
- **OMDb API** - Movie data (recommended)
- **TMDB API** - Alternative movie data source

### Algorithms
- **TF-IDF Vectorization** - Text analysis for genres
- **Cosine Similarity** - Content-based matching
- **K-Nearest Neighbors** - Collaborative filtering
- **Hybrid Recommendation** - Weighted combination

---

## 👥 Authors

- **Harsh Jain** - Initial work

---

## 🙏 Acknowledgments

- MovieLens dataset provided by GroupLens Research
- OMDb API for movie data
- TMDB for alternative movie information
- Flask community for excellent documentation
- Scikit-learn for machine learning tools

---

## 📞 Support

For issues, questions, or suggestions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [API Documentation](#-api-documentation)
3. Ensure all dependencies are installed correctly
4. Verify dataset format matches requirements

---

## 🎓 Learn More

### Recommendation Systems
- [Recommender Systems Handbook](https://www.springer.com/gp/book/9780387858203)
- [Netflix Prize](https://en.wikipedia.org/wiki/Netflix_Prize)
- [Collaborative Filtering Tutorial](https://developers.google.com/machine-learning/recommendation)

### Flask Development
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### Machine Learning
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Understanding TF-IDF](https://monkeylearn.com/blog/what-is-tf-idf/)

---

## 📊 Statistics

- **Lines of Code**: ~2,500
- **Files**: 12
- **Supported Genres**: 18+
- **Recommendation Algorithm**: Hybrid (Content + Collaborative)
- **API Support**: 3 options (OMDb, TMDB, Offline)
- **Responsive**: Yes
- **Mobile Friendly**: Yes

---

## 🎉 Get Started Now!

```bash
# 1. Clone the project
mkdir movie_recommender && cd movie_recommender

# 2. Install dependencies
pip install flask pandas numpy scikit-learn requests

# 3. Get FREE API key (1 minute)
# Visit: http://www.omdbapi.com/apikey.aspx

# 4. Configure
# Add key to config.py

# 5. Run
python app.py

# 6. Enjoy!
# Open http://localhost:5000
```

---

**Built with ❤️ using Flask, Pandas, and Scikit-learn**

**Star this project if you find it helpful! ⭐**
