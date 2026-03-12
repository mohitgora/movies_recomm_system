import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# Page config
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Netflix Dark UI CSS
st.markdown("""
<style>

.stApp {
    background-color: #0f0f0f;
    color: white;
}

h1 {
    color: #E50914;
    text-align: center;
    font-size: 50px;
}

.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 200px;
    font-size: 18px;
}

div[data-baseweb="select"] {
    background-color: #1c1c1c;
    border-radius: 10px;
}

.movie-card {
    background-color: #1c1c1c;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# Download pickle files if not present
if not os.path.exists("movies_dict.pkl"):
    gdown.download("https://drive.google.com/uc?id=1tT1P5za618N5Cr4wiomxHh7C6VH8IecH","movies_dict.pkl",quiet=False)

if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/uc?id=1Dg_qeKY2htFbORiidSRglKmUWQsGcGdg","similarity.pkl",quiet=False)

if not os.path.exists("movies.pkl"):
    gdown.download("https://drive.google.com/uc?id=12U7zhz6rH4oxldE5vvFnTmP4NJroxk9u","movies.pkl",quiet=False)


# Load data
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


# Poster fetch function
def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?api_key=3f666f231d759054c3df8192952f5b63&language=en-US".format(movie_id)

    response = requests.get(url)

    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# Recommendation function
def recommend(movie):

    movie_index = movies[movies['title']==movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []

    recommended_movie_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters


# Title
st.markdown("<h1>🎬 Netflix Style Movie Recommender</h1>", unsafe_allow_html=True)


# Movie selector
selected_movies_name = st.selectbox(
    "Select a movie you like",
    movies['title'].values
)


# Recommendation button
if st.button('Recommend'):

    names, posters = recommend(selected_movies_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
        st.image(posters[0])
        st.write(names[0])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
        st.image(posters[1])
        st.write(names[1])
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
        st.image(posters[2])
        st.write(names[2])
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
        st.image(posters[3])
        st.write(names[3])
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
        st.image(posters[4])
        st.write(names[4])
        st.markdown('</div>', unsafe_allow_html=True)