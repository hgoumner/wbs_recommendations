import streamlit as st

from most_recent_trending import most_recent, most_trending
from funct_item_item      import item_item_recommender
from byuserId             import user_user_recommender

from cover_image import get_imdb_cover_image_url, get_tmdb_cover_image_url

BASE_URL = 'https://www.imdb.com/title/tt'
NF_IMAGE = 'http://www.quickmeme.com/img/bd/bdb7ac37e00ff92776d0dead5171743db339c34a1f4f4c7293b3bde5ca960c79.jpg'
NF_LINK  = 'https://theuselessweb.com/'


# def no_info(col, data, item_id):
def title(data, item_id):
    data = data.copy()
    movie_names = data.drop_duplicates(subset='title')[['imdbId', 'movieId', 'title']]

    movie_missing = movie_names.loc[movie_names['imdbId'] == item_id, 'title']

    title = movie_missing.iloc[0]
    if ', The' in title:
        title = 'The ' + title.split(', The')[0]

    return title


def get_movie_recommendations(cols, data, N, func, database, user_id, item_id):

    if (func.__name__ == 'user_user_recommender'):
        movies = func(data, N, user_id)[database]
    elif (func.__name__ == 'item_item_recommender'):
        movies = func(data, N, item_id)[database]
    else:
        movies = func(data, N)[database]

    if database[0] == 'i':
        get_image = get_imdb_cover_image_url
    else:
        get_image = get_tmdb_cover_image_url

    movies_urls = []
    for item in range(N):
        movies_urls.append(get_image(movies.iloc[item]))

    for index, col in enumerate(cols):
        if movies_urls[index]:
            movies_url       = BASE_URL + str(movies.iloc[index])
            movies_image_url = movies_urls[index]
            col.markdown(f''' <a href={movies_url}><img src="{movies_image_url}" style="width:120px" ></a> ''', unsafe_allow_html=True)
            col.write(f'{title(data, movies.iloc[index])}')
        else:
            # col.markdown(f''' <a><img src="{NF_IMAGE}" style="width:120px" ></a> ''', unsafe_allow_html=True)
            col.image('./not_found.jpg', width=120)
            col.write(f'{title(data, movies.iloc[index])}')


def get_recommendations(data, N, movie_name, item_id, user_id):

    database = 'i' + 'mdbId'

    # user-user
    st.header('Top Picks for Ursula')
    with st.container():
        cols = st.columns(N, gap='large')
        get_movie_recommendations(cols, data, N, user_user_recommender, database, user_id, item_id)

    # most trending
    st.header('Trending now')
    with st.container():
        cols = st.columns(N, gap='large')
        get_movie_recommendations(cols, data, N, most_trending, database, user_id, item_id)

    # item_item
    st.header(f'Because you watched {movie_name}')
    with st.container():
        cols = st.columns(N, gap='large')
        get_movie_recommendations(cols, data, N, item_item_recommender, database, user_id, item_id)

    # most recent
    st.header('New Releases')
    with st.container():
        cols = st.columns(N, gap='large')
        get_movie_recommendations(cols, data, N, most_recent, database, user_id, item_id)
