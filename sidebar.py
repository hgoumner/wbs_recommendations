import streamlit as st


def make_sidebar(names, movie_names, item_ids, user_ids):
    with st.sidebar:
        # number of recommendations
        N = st.number_input('Enter number of recommendations', min_value=1, max_value=10)

        # movie name
        movie_name = st.selectbox('Enter movie name', options=movie_names['title'])
        item_id    = movie_names.loc[movie_names.loc[movie_names['title'] == movie_name, 'movieId'].index[0], 'movieId']

        # user id
        user_name = st.selectbox('Enter reference name', options=names['name'])
        user_id   = names.loc[names.loc[names['name'] == user_name, 'userId'].index[0], 'userId']

    return N, movie_name, item_id, user_id
