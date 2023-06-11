import pandas as pd
from sklearn import set_config
from sklearn.preprocessing import MinMaxScaler
import re

set_config(transform_output='pandas')


def user_user_recommender(data, N, user_id):
    ''' user user recommender '''

    data = data.copy()

    rating_threshold = 3.9
    t1 = 0.1
    t2 = 2.5

    def cleaner(title):
        return re.sub('[^a-zA-Z0-9 ]', ' ', title)

    data['title'] = data['title'].apply(cleaner)

    userId = user_id

    similar_movies = data.loc[(data['userId'] == userId) & (data['rating'] > rating_threshold)]['movieId'].unique()
    rec_scores = data.loc[(data['movieId'].isin(similar_movies)) & (data['rating'] > rating_threshold), 'movieId'].value_counts()
    rec_scores /= data[data['userId'] == userId]['userId'].nunique()
    rec_scores = rec_scores[rec_scores > t1]
    rec_scores_df = pd.DataFrame({'movieId': rec_scores.index, 'score': rec_scores})
    rec_movies = rec_scores_df.merge(data.drop_duplicates(subset='movieId'), on='movieId')

    likedgenres = rec_movies.loc[(rec_movies['userId'] == userId) & (rec_movies['rating'] >= t2)]
    word_counts = {}
    unique_words = set()

    for index, row in likedgenres.iterrows():
        genre_value = row['genres']
        genre_words = genre_value.split('|')
        unique_words.update(genre_words)
        likedgenres_list = list(unique_words)
        for word in genre_words:
            if word in likedgenres_list:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

    data = [{'Genre': word, 'Count': count} for word, count in word_counts.items()]
    df_word_counts = pd.DataFrame(data, columns=['Genre', 'Count'])

    if not df_word_counts.empty:
        scaler = MinMaxScaler()
        count_array = df_word_counts['Count'].values.reshape(-1, 1)
        weights = scaler.fit_transform(count_array)
        df_word_counts['Weights'] = weights
    else:
        df_word_counts['Weights'] = 0.0

    for index, row in rec_movies.iterrows():
        genre_value = row['genres']
        genre_words = genre_value.split('|')
        weight_sum = 0.0
        genre_count = 0

        for word in genre_words:
            if word in df_word_counts['Genre'].values:
                weight = df_word_counts.loc[df_word_counts['Genre'] == word, 'Weights'].values[0]
                weight_sum += weight
                genre_count += 1

        if genre_count != 0:
            rec_movies.at[index, 'Weight'] = weight_sum / genre_count
        else:
            rec_movies.at[index, 'Weight'] = 0.0001

    rec_movies['finet'] = rec_movies['score'] * rec_movies['Weight']

    rec_movies_sorted = rec_movies.sort_values('finet', ascending=False)
    rec_movies_sorted = rec_movies_sorted[['title', 'genres', 'imdbId', 'tmdbId']]

    rec_movies_sorted.drop_duplicates(subset='title', inplace=True)

    return rec_movies_sorted.head(N)