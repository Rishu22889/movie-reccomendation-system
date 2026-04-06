# Movie Recommender System

**Live demo:** https://movie-reccomendation-system-a42c.onrender.com

A content-based movie recommender system built with Streamlit. Just pick a movie and it shows you 5 similar ones along with their posters fetched from TMDB.

## How it works

It uses a bag-of-words approach on movie tags (genres, cast, crew, keywords, etc.) with `CountVectorizer` and computes cosine similarity between movies. When you select a movie and hit Recommend, it finds the 5 most similar movies and pulls their posters from the TMDB API.

## Setup

1. Clone the repo

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Add your TMDB API key in a `.env` file:
   ```
   API_KEY=your_tmdb_api_key_here
   ```
   You can get one for free at [themoviedb.org](https://www.themoviedb.org/settings/api)

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Files

- `app.py` — main Streamlit app
- `movies.pkl` — preprocessed movie dataset with tags
- `similarity.pkl` — precomputed similarity matrix
- `start.sh` — used for deployment (runs on a configurable port)

## Issues & Debugging

**1. similarity.pkl too large for GitHub**

The precomputed similarity matrix (`similarity.pkl`) was 176 MB, which exceeds GitHub's file size limit. To fix this, I removed the file from the repo entirely and moved the similarity computation into the app at runtime, wrapped with `@st.cache_data` so it only runs once per session.

**2. Render free tier hitting 512 MB memory limit**

Computing the full cosine similarity matrix for all movies at once was too heavy — it was loading the entire matrix into memory and crashing on Render's free tier (512 MB limit). To fix this, instead of computing similarity across all movie pairs upfront, I now compute similarity only for the selected movie on demand. This keeps memory usage minimal since we only ever need one row of the similarity matrix at a time.

## Tech Stack

- Python
- Streamlit
- scikit-learn
- pandas
- TMDB API
