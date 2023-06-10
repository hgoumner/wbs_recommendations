import streamlit as st

from most_recent_trending import most_recent, most_trending
from funct_item_item      import item_item_recommender
from byuserId             import user_user_recommender

from cover_image import get_cover_image_url

BASE_URL = 'https://www.imdb.com/title/tt'
NF_IMAGE = 'http://www.quickmeme.com/img/bd/bdb7ac37e00ff92776d0dead5171743db339c34a1f4f4c7293b3bde5ca960c79.jpg'
NF_LINK  = 'https://theuselessweb.com/'

T = 10


def no_info(col, data, item_id):
    data = data.copy()
    movie_names = data.drop_duplicates(subset='title')[['imdbId', 'movieId', 'title']]

    movie_missing = movie_names.loc[movie_names['imdbId'] == item_id, 'title']

    title = movie_missing.iloc[0]
    if ', The' in title:
        title = 'The ' + title.split(', The')[0]
    col.markdown(title)


def get_most_recent(cols, data, N):

    mr = most_recent(data, N)['imdbId']

    mr_urls = []
    for item in range(N):
        mr_urls.append(get_cover_image_url(mr.iloc[item]))

    for index, col in enumerate(cols):
        if mr_urls[index]:
            mr_url       = BASE_URL + str(mr.iloc[index])
            mr_image_url = mr_urls[index]
            col.markdown(f''' <a href={mr_url}><img src="{mr_image_url}" style="width:120px" ></a> ''', unsafe_allow_html=True)
        else:
            # col.markdown(f''' <a href={NF_LINK}><img src="{NF_IMAGE}" style="width:120px" ></a> ''', unsafe_allow_html=True)
            no_info(col, data, mr.iloc[index])


def get_most_trending(cols, data, N, T=10):

    mt = most_trending(data, N, T)['imdbId']

    mt_urls = []
    for item in range(N):
        mt_urls.append(get_cover_image_url(mt.iloc[item]))

    for index, col in enumerate(cols):
        if mt_urls[index]:
            mt_url       = BASE_URL + str(mt.iloc[index])
            mt_image_url = mt_urls[index]
            col.markdown(f''' <a href={mt_url}><img src="{mt_image_url}" style="width:120px" ></a> ''', unsafe_allow_html=True)
        else:
            # col.markdown(f''' <a href={NF_LINK}><img src="{NF_IMAGE}" style="width:120px" ></a> ''', unsafe_allow_html=True)
            no_info(col, data, mt.iloc[index])


def get_user_user(cols, data, N, user_id):

    uu = user_user_recommender(data, N, user_id)['imdbId']

    uu_urls = []
    for item in range(N):
        uu_urls.append(get_cover_image_url(uu.iloc[item]))

    for index, col in enumerate(cols):
        if uu_urls[index]:
            uu_url       = BASE_URL + str(uu.iloc[index])
            uu_image_url = uu_urls[index]
            col.markdown(f''' <a href={uu_url}><img src="{uu_image_url}" style="width:120px" ></a> ''', unsafe_allow_html=True)
        else:
            # col.markdown(f''' <a href={NF_LINK}><img src="{NF_IMAGE}" style="width:120px" ></a> ''', unsafe_allow_html=True)
            no_info(col, data, uu.iloc[index])


def get_item_item(cols, data, N, item_id):

    ii = item_item_recommender(data, N, item_id)['imdbId']

    ii_urls = []
    for item in range(N):
        ii_urls.append(get_cover_image_url(ii.iloc[item]))

    for index, col in enumerate(cols):
        if ii_urls[index]:
            ii_url       = BASE_URL + str(ii.iloc[index])
            ii_image_url = ii_urls[index]
            col.markdown(f''' <a href={ii_url}><img src="{ii_image_url}" style="width:120px" ></a> ''', unsafe_allow_html=True)
        else:
            # col.markdown(f''' <a href={NF_LINK}><img src="{NF_IMAGE}" style="width:120px" ></a> ''', unsafe_allow_html=True)
            no_info(col, data, ii.iloc[index])


def get_recommendations(data, N, movie_name, item_id, user_id):

    # user-user
    st.header('Top Picks for Ursula')
    with st.container():
        cols = st.columns(N, gap='large')
        get_user_user(cols, data, N, user_id)

    # most trending
    st.header('Trending now')
    with st.container():
        cols = st.columns(N, gap='large')
        get_most_trending(cols, data, N, T)

    # item_item
    st.header(f'Because you watched {movie_name}')
    with st.container():
        cols = st.columns(N, gap='large')
        get_item_item(cols, data, N, item_id)

    # most recent
    st.header('New Releases')
    with st.container():
        cols = st.columns(N, gap='large')
        get_most_recent(cols, data, N)
