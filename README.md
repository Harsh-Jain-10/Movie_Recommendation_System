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
