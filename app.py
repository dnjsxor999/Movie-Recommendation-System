# import necessary modules
import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

# make the objects to following tmdbv3api
movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'aa36e26d35e90e051eb3dc0fa667ca6c'

# make the function: get_recommendations(title):
def get_recommendations(title):
    input_idx = movies[movies['title'] == title].index[0]
    # get the index from the title of this movie
    scores_sim = list(enumerate(cosine_sim[input_idx]))
    # get the (index, similarity) from the cosine_similarity, I defines this scores.
    scores_sim = sorted(scores_sim, key=lambda x: x[1], reverse=True) # we need to sort the x[1] (second value) (only for similarity)
    # sort the scores for decending order, targeting to similarity x[1].
    scores_sim = scores_sim[1:11]
    # slice from 1 to 11 for excepting itself.
    get_movie_indices = [i[0] for i in scores_sim]
    # get the indices from scores_sim
    
    # get images and titles from the tmdb api 
    images = []
    titles = []
    for i in get_movie_indices:
        temp_id = movies['id'].iloc[i]
        details = movie.details(temp_id) # details has many attributes and informations of the movie of id
        
        image_path = details['poster_path']
        if image_path :
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else: # when image_path is none
            image_path = 'no_image.jpg'
        images.append(image_path)
        titles.append(details['title'])
    return images, titles

# bring our files with pickle
movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

# make the window by using the streamlit
st.set_page_config(layout='wide')
st.header("Here Taek's Recommendation")

# view movies to combo box on my website
movie_list = movies['title'].values
title_selected = st.selectbox('Choose a movie you like', movie_list)

# make button
if st.button('Recommend'):
    with st.spinner('Please wait...'):
        # get recommendation from my function
        images, titles = get_recommendations(title_selected)
        
        # view the images and titles
        index = 0
        for i in range(0, 2):
            cols = st.columns(5)
            for col in cols:
                col.image(images[index])
                col.write(titles[index])
                index += 1