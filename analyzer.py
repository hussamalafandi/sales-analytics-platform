"""
Data Loading, Cleaning, and Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class DataAnalyzer:
    """A class for loading, cleaning, and analyzing sales data."""
    
    def __init__(self):
        """Initialize the DataAnalyzer with an empty dataframe."""
        self.df = None
    
    def load_data(self, file_path):
        """
        Load data from a CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            The loaded dataframe
        """
        try:
            self.df = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            raise
        return self.df

    def clean_data(self):
        """
        Clean the loaded dataframe.
        
        Performs the following operations:
        - Fills missing values with mean for numerical columns
        - Removes rows with missing values in string columns
        - Converts order_date to datetime
        - Removes duplicates
        
        Returns:
            The cleaned dataframe
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Fill missing values with mean for numerical columns
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            self.df[col] = self.df[col].fillna(self.df[col].mean())

        # Delete rows with missing values in string columns
        string_cols = self.df.select_dtypes(include=[str]).columns
        self.df.dropna(subset=string_cols, inplace=True)

        # Convert date column to datetime
        self.df['order_date'] = pd.to_datetime(self.df['order_date'], errors='coerce')

        # Remove duplicates
        self.df.drop_duplicates(inplace=True)

        return self.df

    def analyze_data(self):
        """
        Analyze the cleaned dataframe and compute key metrics.
        
        Returns:
            A dictionary containing various analytics metrics
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        analytics = {}

        # 1. Total Revenue, Average Order Value & Customer Count
        analytics['total_revenue'] = self.df['order_amount'].sum()
        analytics['average_order_value'] = self.df['order_amount'].mean()
        analytics['customer_count'] = self.df['customer_id'].nunique()

        # 2. Revenue by Category
        analytics['revenue_by_category'] = self.df.groupby('product_category')['order_amount'].sum().to_dict()

        # 3. Top 10 Customers by Lifetime Value
        customer_lifetime_value = self.df.groupby('customer_id')['order_amount'].sum().sort_values(ascending=False)
        analytics['top_customers'] = customer_lifetime_value.head(10).to_dict()

        # 4. Order Status Distribution
        analytics['order_status_distribution'] = self.df['status'].value_counts().to_dict()

        # 5. Average Order Value by Category
        analytics["avg_order_by_category"] = self.df.groupby("product_category")["order_amount"].mean().to_dict()
        
        # 6. Repeat Customer Rate
        total_customers = self.df["customer_id"].nunique()
        repeat_purchases = self.df.groupby("customer_id").size()
        repeat_customers = (repeat_purchases > 1).sum()
        analytics["repeat_customer_rate"] = (repeat_customers / total_customers * 100) if total_customers > 0 else 0
        
        # 7. Monthly Revenue Trends
        monthly_revenue = self.df.groupby(self.df["order_date"].dt.to_period("M"))["order_amount"].sum()
        analytics["monthly_revenue"] = monthly_revenue.to_dict()

        # 8. Outlier Detection (Unusually Large/Small Orders)
        Q1 = self.df['order_amount'].quantile(0.25)
        Q3 = self.df['order_amount'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.df[(self.df['order_amount'] < lower_bound) | (self.df['order_amount'] > upper_bound)]
        analytics['outlier_orders'] = {
            'count': len(outliers),
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound),
            'outlier_details': outliers[['customer_id', 'order_amount', 'product_category', 'status']].to_dict(orient='records') if len(outliers) > 0 else []
        }

        return analytics
    
    def print_analytics(self):
        """Print the analytics metrics in a readable format."""
        analytics = self.analyze_data()

        print("=== Sales Analytics ===")
        print("="*60)

        print(f"Total Revenue: ${analytics['total_revenue']:.2f}")
        print(f"Average Order Value: ${analytics['average_order_value']:.2f}")
        print(f"Customer Count: {analytics['customer_count']}")

        print("\nRevenue by Category:")
        for category, revenue in analytics['revenue_by_category'].items():
            print(f"  {category}: ${revenue:.2f}")

        print("\nTop 10 Customers by Lifetime Value:")
        for customer_id, ltv in analytics['top_customers'].items():
            print(f"  Customer {customer_id}: ${ltv:.2f}")
            
        print("\nOrder Status Distribution:")
        for status, count in analytics['order_status_distribution'].items():
            print(f"  {status}: {count} orders")
        
        print("\nMonthly Revenue Trends:")
        for month, revenue in analytics["monthly_revenue"].items():
            print(f"  {month}: ${revenue:.2f}")
        
        print("\nOutlier Orders:")
        print(f"  Count: {analytics['outlier_orders']['count']}")
        print(f"  Lower Bound: ${analytics['outlier_orders']['lower_bound']:.2f}")
        print(f"  Upper Bound: ${analytics['outlier_orders']['upper_bound']:.2f}")
        if analytics['outlier_orders']['count'] > 0:
            print("  Outlier Details:")
            for outlier in analytics['outlier_orders']['outlier_details']:
                print(f"    Customer ID: {outlier['customer_id']}, Order Amount: ${outlier['order_amount']:.2f}, Category: {outlier['product_category']}, Status: {outlier['status']}")
            
        print("\n" + "="*60)