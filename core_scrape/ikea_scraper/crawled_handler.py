import pandas as pd

def removeDuplicates(csv_file, column_name):
    df = pd.read_csv(csv_file)

    # drop any duplicate category_urls
    df = df.drop_duplicates(subset=column_name, keep='first')
    df.to_csv(csv_file)