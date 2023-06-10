import pandas as pd


def item_item_recommender(data, N, item_id):
    ''' item-item based recommender '''

    data = data.copy()

    threshold = 0.8

    movies_crosstab          = pd.pivot_table(data=data, values='rating', index='userId', columns='movieId')
    inputed_movie_rating     = movies_crosstab[item_id]
    similar_to_inputed_movie = movies_crosstab.corrwith(inputed_movie_rating)

    corr_inputed_movie       = pd.DataFrame(similar_to_inputed_movie, columns=['PearsonR'])
    corr_inputed_movie.dropna(inplace=True)
    corr_inputed_movie.drop(item_id, inplace=True)

    top_n = corr_inputed_movie[corr_inputed_movie['PearsonR'] >= threshold].sort_values('PearsonR', ascending=False)

    top_n_movies = top_n.merge(data, left_index=True, right_on="movieId")
    top_n_movies.drop_duplicates(subset='title', inplace=True)

    return top_n_movies.head(N)