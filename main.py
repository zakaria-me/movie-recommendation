import pandas as pd

# Get user fav movies list
user_fav_movies = pd.read_csv('fav-movies.csv')

# Get movie db
movie_db = pd.read_csv('../ml-latest/movies.csv')

# Only get movies seen by the user
fav_movies_info = pd.merge(left=movie_db, right=user_fav_movies, on='movieId')

# Get genres
fav_genres = fav_movies_info.get('genres')

# Get most popular genre 
genres_dict = dict()
for row in fav_genres:
    row = row.split('|')
    for genre in row:
        if genre in genres_dict:
            genres_dict[genre] += 1
        else:
            genres_dict[genre] = 1

max_value = 0
most_popular_genre = ""
for genre in genres_dict:
    if genres_dict[genre] > max_value:
        max_value = genres_dict[genre]
        most_popular_genre = genre

# Get Movie of same genre
most_popular_genre_movies = pd.DataFrame()
for index in range(len(movie_db.index)):
    if movie_db.iloc[index].get('genres').find('Animation') != -1:
        most_popular_genre_movies = most_popular_genre_movies.append(movie_db.iloc[index])

movie_ratings=pd.read_csv('../ml-latest/ratings.csv')

# Get average ratings of theses movies
most_popular_genre_movies_ratings = pd.merge(left=movie_ratings, right=most_popular_genre_movies, on='movieId')

avg_ratings = most_popular_genre_movies_ratings.groupby(['movieId','title'])['rating'].mean()

# get most popular movie
recommended_movie = most_popular_genre_movies_ratings.groupby(['movieId','title']).mean()["rating"].idxmax()

# get rating 
recommended_movie_rating = avg_ratings.loc[avg_ratings.idxmax()[0], avg_ratings.idxmax()[1]]

print("We recommend you : " + recommended_movie[1] + ". Which has an average rating of : " + str(recommended_movie_rating))