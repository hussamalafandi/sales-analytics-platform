import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("./data/sales_data.csv")

# 1. Data Cleaning
# Check info missing values and data types
print(df.info())

# Fill missing values with mean for numerical columns
numerical_cols = df.select_dtypes(include=[np.number]).columns
for col in numerical_cols:
    df[col] = df[col].fillna(df[col].mean())

# Delete rows with missing values in string columns
string_cols = df.select_dtypes(include=[str]).columns
df.dropna(subset=string_cols, inplace=True)

# Convert date column to datetime
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

print(df.info())