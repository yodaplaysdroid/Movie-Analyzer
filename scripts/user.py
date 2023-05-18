import pandas as pd
import scripts.recommender as Recommender


class User:

    def __init__(self, id):
        self.id = id
        self.path = 'data/ratings/' + str(self.id) + '.csv'
    
    
    def __recently_watched(self):
        df = pd.read_csv(self.path)
        watched = df.sort_values('timestamp', ascending=False)[0:10]
        self.watched = watched.movieId.tolist()

        return watched


    def __movie_genres(self):

        self.__recently_watched()

        genres = []
        sorted_movie_ids = self.watched.copy()
        sorted_movie_ids.sort()
        movie_ids_arrangements = []

        for id in sorted_movie_ids:
            movie_ids_arrangements.append(self.watched.index(id))

        chunksize = 10 ** 6

        for chunk in pd.read_csv('data/ml-25m/movies.csv', chunksize=chunksize):
            if len(sorted_movie_ids) == 0:
                break

            for index, row in chunk.iterrows():
                if len(sorted_movie_ids) == 0:
                    break
                if sorted_movie_ids[0] == row[0]:
                    genres.append(row[2])
                    sorted_movie_ids.pop(0)

        temp_dict = {'genres':genres, 'arrangement':movie_ids_arrangements}
        df = pd.DataFrame(temp_dict)
        df = df.sort_values('arrangement', ascending=True)
        temp = df['genres'].tolist()

        genres = []
        for genre in temp:
            temp1 = genre.split('|')
            genres = genres + temp1

        genre_count = pd.DataFrame(genres, columns=['genre'])
        genre_count['count'] = 1
        genre_count = genre_count.groupby('genre').count().reset_index(names='genre')

        self.fav_genre = genre_count.sort_values('count', ascending=False)['genre'][0:5].tolist()

        return genre_count.sort_values('count', ascending=False)[0:5]


    def recommend(self):

        self.__movie_genres()

        chunksize = 10 ** 6
        movies = []
        
        for chunk in pd.read_csv('data/ml-25m/movies.csv', chunksize=chunksize):
            for index, row in chunk.iterrows():
                for fav in self.fav_genre:
                    if fav in row[2]:
                        movies.append(row[1])
        
        movies = pd.DataFrame(movies, columns=['title'])
        movies['count'] = 1
        relevance = movies.groupby('title')['count'].count().reset_index()
        relevance = relevance.sort_values('count', ascending=False)
        
        ratings = pd.read_csv('data/score.csv')
        ratings = relevance.merge(ratings, on='title')
        ratings['score'] = ratings['count'] * 0.2 + ratings['total'] * 0.8
        ratings = ratings.sort_values('score', ascending=False)
        movies = ratings['title'].iloc[0:10].tolist()
        return Recommender.get_unique(movies)


if __name__ == '__main__':
    pass
