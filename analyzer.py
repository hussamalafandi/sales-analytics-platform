"""
Data Loading, Cleaning, and Analysis
"""

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

def analyze_data(df):
    analytics = {}

    # 1. Total Revenue, Average Order Value & Customer Count
    analytics['total_revenue'] = df['order_amount'].sum()
    analytics['average_order_value'] = df['order_amount'].mean()
    analytics['customer_count'] = df['customer_id'].nunique()

    # 2. Revenue by Category
    analytics['revenue_by_category'] = df.groupby('product_category')['order_amount'].sum().to_dict()

    # 3. Top 10 Customers by Lifetime Value
    customer_lifetime_value = df.groupby('customer_id')['order_amount'].sum().sort_values(ascending=False)
    analytics['top_customers'] = customer_lifetime_value.head(10).to_dict()

    # 4. Order Status Distribution
    analytics['order_status_distribution'] = df['status'].value_counts().to_dict()

    # 5. Average Order Value by Category
    analytics["avg_order_by_category"] = df.groupby("product_category")["order_amount"].mean().to_dict()
    
    # 6. Repeat Customer Rate
    total_customers = df["customer_id"].nunique()
    repeat_purchases = df.groupby("customer_id").size()
    repeat_customers = (repeat_purchases > 1).sum()
    analytics["repeat_customer_rate"] = (repeat_customers / total_customers * 100) if total_customers > 0 else 0
    
    # 7. Monthly Revenue Trends
    monthly_revenue = df.groupby(df["order_date"].dt.to_period("M"))["order_amount"].sum()
    analytics["monthly_revenue"] = monthly_revenue.to_dict()

    return analytics