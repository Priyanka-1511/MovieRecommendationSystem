import streamlit as st
import pickle
import requests

# Load data
try:
    df = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))
except FileNotFoundError as e:
    st.write(f"Error loading files: {e}")
    st.stop()

movies_list = df['title'].values

st.header("Movie Recommendation System")
selectvalue = st.selectbox("Select movie from dropdown", movies_list)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY" 
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def recommend(movie):
    if movie not in df['title'].values:
        st.write("Movie not found in the list.")
        return [], []
    
    index = df[df['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movie_id = df.iloc[i[0]].id
        recommend_movie.append(df.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    if movie_name:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(movie_name[0])
            st.image(movie_poster[0])
        with col2:
            st.text(movie_name[1])
            st.image(movie_poster[1])
        with col3:
            st.text(movie_name[2])
            st.image(movie_poster[2])
        with col4:
            st.text(movie_name[3])
            st.image(movie_poster[3])
        with col5:
            st.text(movie_name[4])
            st.image(movie_poster[4])