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
data        = pd.read_csv('recommendations/app/full_data.csv')
item_ids    = list(data['movieId'].unique())
user_ids    = list(data['userId'].unique())
movie_names = data.drop_duplicates(subset='title')[['movieId', 'title']]

# sidebar
# --------------------------------------------------------
N, movie_name, item_id, user_id = make_sidebar(movie_names, item_ids, user_ids)

# Get recommendations
# --------------------------------------------------------
get_recommendations(data, N, movie_name, item_id, user_id)
