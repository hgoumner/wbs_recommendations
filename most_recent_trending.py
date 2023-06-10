# Functions to get most recent and most trending movies


def most_recent(data, N):
    ''' get N most recent movies '''

    data = data.copy()

    # get only unique values and sort descendingly by year
    data.drop_duplicates(subset='title', inplace=True)
    data.dropna(subset='year', inplace=True)
    data.sort_values(by='year', ascending=False, inplace=True)

    return data.head(N)


def most_trending(data, N, time_period):
    ''' get N most trending movies within last time_period years'''

    data = data.copy()

    # get only unique values and sort descendingly by year
    data.drop_duplicates(subset='title', inplace=True)
    data.dropna(subset='year', inplace=True)

    # slice out data for given time period
    max_year = max(data['year'])
    min_year = max_year - time_period
    sliced = data.loc[data['year'] >= min_year].copy()

    sliced.sort_values(by=['rating_count', 'year'], ascending=False, inplace=True)

    return sliced.head(N)