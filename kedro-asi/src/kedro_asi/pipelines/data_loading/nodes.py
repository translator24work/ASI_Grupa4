import pandas as pd
import os


def save_data_to_file(df, path):
    if not os.path.exists("data"):
        os.makedirs("data")
    df.to_csv(path, index=False)


def read_data(url, path) -> pd.DataFrame:
    df = pd.read_csv(url)
    save_data_to_file(df, path)
    return df
