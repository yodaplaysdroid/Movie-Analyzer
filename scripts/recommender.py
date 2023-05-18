import pandas as pd
import time
import pickle
from pathlib import Path
import os


# getting unique list
# input  : list<any>
# output : list<any>
def get_unique(input_list):

    unique_list = []
    seen = set()

    for item in input_list:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)

    return unique_list


# movie_id to name conversion
# input  : list<movie_ids>
# output : list<movie_names>
def movie_id_to_movie_name(movie_ids):

    movies = []
    sorted_movie_ids = movie_ids.copy()
    sorted_movie_ids.sort()
    movie_ids_arrangements = []

    for id in sorted_movie_ids:
        movie_ids_arrangements.append(movie_ids.index(id))
        
    chunksize = 10 ** 6

    for chunk in pd.read_csv('data/ml-25m/movies.csv', chunksize=chunksize):
        if len(sorted_movie_ids) == 0:
            break

        for index, row in chunk.iterrows():
            if len(sorted_movie_ids) == 0:
                break
            if sorted_movie_ids[0] == row[0]:
                movies.append(row[1])
                sorted_movie_ids.pop(0)

    temp_dict = {'movies':movies, 'arrangement':movie_ids_arrangements}
    df = pd.DataFrame(temp_dict)
    df = df.sort_values('arrangement', ascending=True)
    movies = df['movies'].tolist()

    return movies


# search movies according to input tag
# input  : string<tag>
# output : list<movie_ids>
def search_movie_tag(input_phrase, extended=False):

    if extended:
        separated_input_phrase = input_phrase.split()
    filtered_movie_id_1 = []
    filtered_movie_id_2 = []
    chunksize = 10 ** 6

    for chunk in pd.read_csv('data/ml-25m/tags.csv', chunksize=chunksize):

        for index, row in chunk.iterrows():
            if input_phrase in str(row[2]):
                filtered_movie_id_1.append(row[1])
            if extended:

                for words in separated_input_phrase:
                    if words in str(row[2]):
                        filtered_movie_id_2.append(row[1])

    filtered_movie_id = get_unique(filtered_movie_id_1) + get_unique(filtered_movie_id_2)
    
    return filtered_movie_id


# movies related to given genome_tags
# input  : list<genome_tag_ids>
# output : list<movie_ids>
def genome_tag_to_movie_id(tags):

    movies_id = []
    movies_relevance = []

    for tag in tags:
        prefix = f'{tag}_'
        file_list = os.listdir('data/genome_scores')
        matching_files = [f for f in file_list if f.startswith(prefix)]
        
        for csv_file in matching_files:
            df = pd.read_csv(f'data/genome_scores/{csv_file}')
            movies_id = movies_id + df['movieId'].tolist()
            movies_relevance = movies_relevance + df['relevance'].tolist()

    temp_dict = {'movie_id':movies_id, 'relevance':movies_relevance}
    df = pd.DataFrame(temp_dict).sort_values('relevance', ascending=False)
    df = df.loc[df['relevance'] >= 0.5]
    filtered_movies_id = df.movie_id.unique().tolist()

    return filtered_movies_id


# filter genome tags
# from input phrase, get related genome tags
# input  : string<input>
# output : list<genome_tag_ids>
def search_genome_tag(input_phrase, extended=False):

    if extended:
        separated_input_phrase = input_phrase.split()
    filtered_tag_id_1 = []
    filtered_tag_id_2 = []
    chunksize = 10 ** 6

    for chunk in pd.read_csv('data/ml-25m/genome-tags.csv', chunksize=chunksize):
        
        for index, row in chunk.iterrows():
                if input_phrase in str(row[1]):
                    filtered_tag_id_1.append(row[0])
                if extended:

                    for words in separated_input_phrase:
                        if words in str(row[1]):
                            filtered_tag_id_2.append(row[0])

    filtered_tag_id = filtered_tag_id_1 + filtered_tag_id_2

    return get_unique(filtered_tag_id)


# movie name searching
# input  : string<input>
# output : list<movie_names>
def search_movie_name(input_phrase, extended=False):

    if extended:
        separated_input_phrase = input_phrase.split()
    filtered_movie_names_1 = []
    filtered_movie_names_2 = []
    chunksize = 10 ** 6

    for chunk in pd.read_csv('data/ml-25m/movies.csv', chunksize=chunksize):

        for index, row in chunk.iterrows():
            if input_phrase in str(row[1]):
                filtered_movie_names_1.append(row[1])
            if extended:

                for words in separated_input_phrase:
                    if words in str(row[1]):
                        filtered_movie_names_2.append(row[1])

    filtered_movie_names = get_unique(filtered_movie_names_1) + get_unique(filtered_movie_names_2)
    
    return filtered_movie_names


# main search function
# from input string search for related movies including tags, genome tags
# input  : string<phrase>
# output : list<movie_names>
def search(input_phrase, extended=False):
    
    path = 'data/cache/' + input_phrase
    if Path(path).is_file():
        with open(path, 'rb') as fp:
            return pickle.load(fp)

    movie_names = search_movie_name(input_phrase, extended)

    genome_tags = search_genome_tag(input_phrase, extended)
    temp = genome_tag_to_movie_id(genome_tags)
    temp = movie_id_to_movie_name(temp)
    movie_names = movie_names + temp

    movie_tags = search_movie_tag(input_phrase, extended)
    temp = movie_id_to_movie_name(movie_tags)
    movie_names = movie_names + temp
    movie_names = list(set(movie_names))

    with open(path, 'wb') as fp:
        pickle.dump(movie_names, fp)

    return movie_names


if __name__ == '__main__':
    start_time = time.time()

    # pass

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(elapsed_time)
