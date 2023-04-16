import recommender
import os

if __name__ == '__main__':
    os.system('cls')
    print('Movie Recommender:')
    print('------------------------------')
    input_phrase = input('Search: ')
    recommended_movies = recommender.search(input_phrase)
    for movie in recommended_movies:
        print(movie)