import pandas as pd
import datetime
import os


def csv_to_df(source):
    try:
        df = pd.read_csv(source)
        return df
    except Exception as e:
        print(f"Error: {e}")

def clean_data(source):
    try:
        df = csv_to_df(source)

        df.dropna(inplace=True)
        price_parts = df['price'].str.split(r' - |\n', expand=True)

        df['min_price'] = price_parts[0].str.extract(r'(\d+\.\d+)').astype(float)
        df['max_price'] = price_parts[1].str.extract(r'(\d+\.\d+)').astype(float)

        df['max_price'].fillna(df['min_price'], inplace=True)

        df.loc[df['min_price'] > df['max_price'], ['min_price', 'max_price']] = df.loc[df['min_price'] > df['max_price'], ['max_price', 'min_price']].values

        df['max_price'] = df['max_price'] * 1000
        df['min_price'] = df['min_price'] * 1000

        df.drop(columns=['price'], inplace=True)

        df['sold_quantity'] = df['sold_quantity'].astype(str)
        df['sold_quantity'] = df['sold_quantity'].str.replace('Đã bán', '')
        df['sold_quantity'] = df['sold_quantity'].str.replace(',', '.')
        df['sold_quantity'] = df['sold_quantity'].str.extract('(\d+\.?\d*)', expand=False)

        df['sold_quantity'] = pd.to_numeric(df['sold_quantity'])

        df['sold_quantity'] = df['sold_quantity'] * 1000

        df['get_at'] = datetime.datetime.now()
        df['gender'] = source.split("_")[0]

        return df

    except Exception as e:
        print(f"Error: {e}")



def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"Not found file: {file_path}")
    except Exception as e:
        print(f"Error {file_path}: {e}")