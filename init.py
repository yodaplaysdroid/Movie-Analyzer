import pandas as pd


if __name__ == '__main__':
    chunk_size = 10 ** 6
    df = pd.read_csv('raw/genome-scores.csv', chunksize=chunk_size)

    for i, chunk in enumerate(df):
        grouped = chunk.groupby('tagId')
        
        # Loop over each group in the chunk
        for name, group in grouped:
            # Define the output filename for the group
            filename = f'genome_scores/{name}_{i}.csv'
            
            # Write the group to a separate CSV file
            group.to_csv(filename, index=False)
