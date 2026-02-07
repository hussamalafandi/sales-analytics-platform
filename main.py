import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        raise
    return df

def clean_data(df):
    # Fill missing values with mean for numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        df[col] = df[col].fillna(df[col].mean())

    # Delete rows with missing values in string columns
    string_cols = df.select_dtypes(include=[str]).columns
    df.dropna(subset=string_cols, inplace=True)

    # Convert date column to datetime
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    return df

try:
    df = load_data('./data/sales_dataa.csv')
except FileNotFoundError:
    exit(1)

df = clean_data(df)
print(df.info())
