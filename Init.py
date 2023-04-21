import pandas as pd
import pickle
import os
import shutil
import time


# initialization
def initialize():

    os.system('cls')
    print('Repairing files ...\n\n')
    start_time = time.time()

    try:
        os.mkdir('genome_scores')
        print('Created : genome_scores')
    except Exception as e:
        # print(e)
        print('Error : genome_scores Exists')

    chunk_size = 10 ** 6
    print('Reading files...')
    
    df = pd.read_csv('raw/genome-scores.csv', chunksize=chunk_size)

    for i, chunk in enumerate(df):
        grouped = chunk.groupby('tagId')
        
        for name, group in grouped:
            filename = f'genome_scores/{name}_{i}.csv'
            group.to_csv(filename, index=False)
            print(f'Created : {filename}')
    
    try:
        os.mkdir('ratings')
        print('Created : ratings')
    except Exception as e:
        # print(e)
        print('Error : ratings Exists')
    
    print('Reading files...')

    df = pd.read_csv('raw/ratings.csv')
    grouped = df.groupby('userId')
    
    for name, group in grouped:
        filename = f'ratings/{name}.csv'
        group.to_csv(filename, index=False)
        print(f'Created : {filename}')
    
    try:
        os.mkdir('scripts/cache')
        print('Created : scripts/cache')
    except Exception as e:
        # print(e)
        print('Error : scripts/cache Exists')
    
    print('Reading Movies Database...')
    ratings = pd.read_csv('raw/ratings.csv')
    rating_count = ratings.groupby('movieId')['rating'].count().reset_index(name='rating_count')
    rating_avg = ratings.groupby('movieId')['rating'].mean().reset_index(name='rating_avg')
    movies = pd.read_csv('raw/movies.csv')
    score = rating_count.merge(rating_avg, on='movieId')
    score = score.merge(movies, on='movieId')
    r = 3
    w = 1000
    score['total'] = (w*r + score['rating_count']*score['rating_avg']) / (w + score['rating_count'])
    score = score.sort_values('total', ascending=False)
    score.to_csv('score.csv', index=False)
    
    end_time = time.time()
    time_taken = end_time - start_time
    print('\n\nOperation finished')
    print(f'Time Taken : {time_taken}s')
    input('Press any key to continue >> ')



# cache clearing
def clear_cache():

    try:
        shutil.rmtree('scripts/cache')
        print('Cache Cleared')
    except Exception as e:
        print('No Cache')
    
    os.mkdir('scripts/cache')


if __name__ == '__main__':
    pass
