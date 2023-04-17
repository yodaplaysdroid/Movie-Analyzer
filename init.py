import pandas as pd
import pickle


if __name__ == '__main__':
    chunk_size = 10 ** 6
    df = pd.read_csv('raw/genome-scores.csv', chunksize=chunk_size)

    for i, chunk in enumerate(df):
        grouped = chunk.groupby('tagId')
        
        for name, group in grouped:
            filename = f'genome_scores/{name}_{i}.csv'
            group.to_csv(filename, index=False)
