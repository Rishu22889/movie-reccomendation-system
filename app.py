import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

api_key = os.getenv('API_KEY')

@st.cache_data
def load_data():
    return pd.DataFrame(pickle.load(open("movies.pkl", 'rb')))

@st.cache_data
def compute_vectors(movies):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    return cv.fit_transform(movies['tags'])


movies = load_data()
vectors = compute_vectors(movies)

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Select Movie: ',
    movies['title'].values
)

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US")
    data = response.json()
    if data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
  movie_index = movies[movies['title'] == movie].index[0]
  similarity = cosine_similarity(vectors[movie_index], vectors).flatten()
  movies_list = sorted(list(enumerate(similarity)), reverse=True, key=lambda x:x[1])[1:6]
  
  recommend_movies = []
  recommend_movies_posters = []

  for i in movies_list:
    movie_id = movies.iloc[i[0]].movie_id
    recommend_movies.append(movies.iloc[i[0]].title)
    recommend_movies_posters.append(fetch_poster(movie_id))
  
  return recommend_movies, recommend_movies_posters


if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])
    
    with col3:
        st.text(names[2])
        st.image(posters[2])
    
    with col4:
        st.text(names[3])
        st.image(posters[3])
    
    with col5:
        st.text(names[4])
        st.image(posters[4])