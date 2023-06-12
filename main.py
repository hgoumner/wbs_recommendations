# Import modules
# --------------------------------------------------------
import streamlit as st
st.set_page_config(layout="wide")

import time
import pandas as pd

from sidebar         import make_sidebar
from recommendations import get_recommendations

# Load data
# --------------------------------------------------------
data        = pd.read_csv('./full_data.csv')
names       = pd.read_csv('./famous.csv')
names       = names.sort_values(by='name', ascending=True)
item_ids    = list(data['movieId'].unique())
user_ids    = list(data['userId'].unique())
movie_names = data.drop_duplicates(subset='title')[['movieId', 'title']]
movie_names = movie_names.sort_values(by='title', ascending=True)

# sidebar
# --------------------------------------------------------
N, movie_name, item_id, user_id = make_sidebar(names, movie_names, item_ids, user_ids)

# Get recommendations
# --------------------------------------------------------
get_recommendations(data, N, movie_name, item_id, user_id)
