"""
setup.py - Automated setup script for Movie Recommendation System
Run this file to automatically set up the project structure
"""

import os
import sys

def create_directory_structure():
    """Create all required directories"""
    directories = [
        'data',
        'templates',
        'static',
        'static/css',
        'static/js'
    ]
    
    print("Creating directory structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ Created {directory}/")
    print()

def create_requirements_file():
    """Create requirements.txt"""
    requirements = """flask==3.0.0
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
requests==2.31.0
"""
    
    print("Creating requirements.txt...")
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("  ✓ Created requirements.txt")
    print()

def create_config_file():
    """Create config.py template"""
    config = """# Configuration file for Movie Recommendation System

# TMDB API Configuration
# Get your API key from: https://www.themoviedb.org/settings/api
TMDB_API_KEY = "YOUR_TMDB_API_KEY_HERE"  # Replace with your actual key
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Application Settings
SECRET_KEY = "your-secret-key-change-in-production"
DEBUG = True

# Recommendation Engine Parameters
CONTENT_WEIGHT = 0.7  # 70% content-based filtering
COLLABORATIVE_WEIGHT = 0.3  # 30% collaborative filtering
MIN_SEED_RATINGS = 3  # Minimum ratings required from user
"""
    
    if not os.path.exists('config.py'):
        print("Creating config.py...")
        with open('config.py', 'w') as f:
            f.write(config)
        print("  ✓ Created config.py")
        print("  ⚠ Remember to add your TMDB API key!")
        print()
    else:
        print("  ℹ config.py already exists, skipping...")
        print()

def create_gitignore():
    """Create .gitignore file"""
    gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Flask
instance/
.webassets-cache

# Config
config.py

# Data
data/*.csv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"""
    
    print("Creating .gitignore...")
    with open('.gitignore', 'w') as f:
        f.write(gitignore)
    print("  ✓ Created .gitignore")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠ Warning: Python 3.8 or higher is recommended")
        print(f"  Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True

def install_dependencies():
    """Install required packages"""
    print("\nDo you want to install dependencies now? (y/n): ", end='')
    choice = input().strip().lower()
    
    if choice == 'y':
        print("\nInstalling dependencies...")
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
        print("\n✓ Dependencies installed!")
    else:
        print("\n  Run 'pip install -r requirements.txt' later to install dependencies")

def download_dataset_instructions():
    """Print instructions for downloading dataset"""
    print("\n" + "="*70)
    print("DATASET SETUP OPTIONS")
    print("="*70)
    print("\nOption 1: Use Dummy Data (Default)")
    print("  - The system will automatically create sample data")
    print("  - Good for testing (50 movies)")
    print("  - No additional setup needed")
    print("\nOption 2: Use MovieLens Dataset (Recommended)")
    print("  - Download from: https://grouplens.org/datasets/movielens/")
    print("  - Get 'ml-latest-small.zip' (100K ratings)")
    print("  - Extract and copy:")
    print("    • ml-latest-small/movies.csv → data/movies_dataset.csv")
    print("    • ml-latest-small/ratings.csv → data/ratings_dataset.csv")
    print("\nOption 3: Use Custom Dataset")
    print("  - Create CSV files with required columns:")
    print("    • movies_dataset.csv: movieId, title, genres")
    print("    • ratings_dataset.csv: userId, movieId, rating")
    print("="*70)

def create_run_script():
    """Create a run script for easy startup"""
    run_script = """#!/usr/bin/env python3
\"\"\"
Quick run script for Movie Recommendation System
\"\"\"

import subprocess
import sys

if __name__ == '__main__':
    print("🎬 Starting Movie Recommendation System...")
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\\n\\n👋 Server stopped. Thanks for using Movie Recommender!")
"""
    
    print("Creating run script...")
    with open('run.py', 'w') as f:
        f.write(run_script)
    
    # Make executable on Unix systems
    if sys.platform != 'win32':
        os.chmod('run.py', 0o755)
    
    print("  ✓ Created run.py")
    print()

def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print("\nNext Steps:")
    print("\n1. Add TMDB API Key (Optional but Recommended):")
    print("   - Open config.py")
    print("   - Replace YOUR_TMDB_API_KEY_HERE with your actual key")
    print("   - Get key from: https://www.themoviedb.org/settings/api")
    
    print("\n2. Set Up Dataset (Optional):")
    print("   - System works with dummy data by default")
    print("   - For better results, download MovieLens dataset")
    print("   - See instructions above")
    
    print("\n3. Create HTML Templates:")
    print("   - Copy HTML code from provided artifacts")
    print("   - Save to templates/ directory:")
    print("     • index.html")
    print("     • step1_genres.html")
    print("     • step2_ratings.html")
    print("     • step3_context.html")
    print("     • results.html")
    
    print("\n4. Create CSS File:")
    print("   - Copy CSS code from provided artifact")
    print("   - Save to static/css/style.css")
    
    print("\n5. Copy Main Application Files:")
    print("   - Save app.py (Flask application)")
    print("   - Save recommender.py (recommendation engine)")
    
    print("\n6. Run the Application:")
    print("   python app.py")
    print("   or")
    print("   python run.py")
    
    print("\n7. Access the Application:")
    print("   Open browser: http://localhost:5000")
    
    print("\n" + "="*70)
    print("📚 Documentation: See README.md for full details")
    print("🔧 API Docs: http://localhost:5000/api/recommend")
    print("💚 Health Check: http://localhost:5000/health")
    print("="*70 + "\n")

def main():
    """Main setup function"""
    print("\n" + "="*70)
    print("🎬 MOVIE RECOMMENDATION SYSTEM - SETUP")
    print("="*70 + "\n")
    
    # Check Python version
    check_python_version()
    print()
    
    # Create structure
    create_directory_structure()
    create_requirements_file()
    create_config_file()
    create_gitignore()
    create_run_script()
    
    # Install dependencies
    install_dependencies()
    
    # Show dataset instructions
    download_dataset_instructions()
    
    # Print next steps
    print_next_steps()

if __name__ == '__main__':
    main()


# ============================================================================
# FILE: requirements.txt (separate file)
# ============================================================================
"""
Save this as requirements.txt:

flask==3.0.0
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
requests==2.31.0
"""

# ============================================================================
# FILE: .env.example (separate file)
# ============================================================================
"""
Save this as .env.example:

# TMDB API Configuration
TMDB_API_KEY=your_api_key_here

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Server Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
"""
