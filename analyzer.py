"""
Data Loading, Cleaning, and Analysis
Demonstrates: Pandas, NumPy, data validation, and business analytics
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict
from models import Product, Service, Customer, RegularCustomer, PremiumCustomer, CorporateCustomer, Order


class SalesAnalyzer:
    """Orchestrates data loading, cleaning, and analysis"""
    
    def __init__(self, csv_path: str):
        """
        Initialize analyzer with a CSV file path
        
        Args:
            csv_path: Path to the sales_data.csv file
        """
        self.csv_path = csv_path
        self.raw_df = None
        self.df = None  # Cleaned data
        self.products = {}  # Dictionary of Product objects by ID
        self.customers = {}  # Dictionary of Customer objects by ID
        self.orders = []  # List of Order objects
    
    def _build_product_from_row(self, product_name: str, category: str, 
                                unit_price: float) -> Product:
        """
        Build a Product object from CSV data.
        Demonstrates object instantiation from dataset.
        """
        product_id = f"PROD_{category}_{product_name.replace(' ', '_')}"
        try:
            return Product(product_id, product_name, category, unit_price)
        except ValueError:
            return None
    
    def _build_customer_from_id(self, customer_id: str, 
                               customer_orders: pd.DataFrame) -> Customer:
        """
        Build a Customer object from aggregated data.
        
        Demonstrates polymorphism: Creates different customer types based on
        lifetime value, showing how different customer tiers have different
        discount rates through method overriding.
        
        Customer Tiers:
        - Regular: < $5,000 LTV
        - Premium: $5,000 - $50,000 LTV  
        - Corporate: >= $50,000 LTV
        """
        ltv = customer_orders["order_amount"].sum()
        
        try:
            # Create different customer types based on lifetime value
            # This demonstrates polymorphism in action
            if ltv >= 50000:
                # Corporate customer: volume-based discount
                customer = CorporateCustomer(
                    id=customer_id,
                    name=f"Company {customer_id}",
                    email=f"{customer_id.lower()}@company.com",
                    lifetime_value=ltv,
                    company_name=f"Corp {customer_id}",
                    annual_volume=ltv
                )
            elif ltv >= 5000:
                # Premium customer: loyalty-based discount
                years = max(1, int(ltv / 10000))  # Estimate years based on LTV
                customer = PremiumCustomer(
                    id=customer_id,
                    name=f"VIP {customer_id}",
                    email=f"{customer_id.lower()}@vip.com",
                    lifetime_value=ltv,
                    years_member=years
                )
            else:
                # Regular customer: no discount
                customer = RegularCustomer(
                    id=customer_id,
                    name=f"Customer {customer_id}",
                    email=f"{customer_id.lower()}@sales.com",
                    lifetime_value=ltv
                )
            return customer
        except ValueError:
            return None
    
    def _build_order_from_row(self, row: pd.Series) -> Order:
        """
        Build an Order object from a DataFrame row.
        Demonstrates OOP validation during object creation.
        """
        try:
            return Order(
                id=row["order_id"],
                date=row["order_date"],
                customer_id=row["customer_id"],
                amount=row["order_amount"],
                status=row["status"]
            )
        except (ValueError, KeyError, TypeError):
            return None
    
    def load_data(self) -> pd.DataFrame:
        """Load and inspect the raw data"""
        print(f"\n📥 Loading data from {self.csv_path}...")
        self.raw_df = pd.read_csv(self.csv_path)
        
        print(f"   Rows: {len(self.raw_df)} | Columns: {len(self.raw_df.columns)}")
        print(f"\n   Data types:\n{self.raw_df.dtypes}")
        print(f"\n   Missing values:\n{self.raw_df.isnull().sum()}")
        
        return self.raw_df
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and validate data:
        1. Remove duplicates
        2. Handle missing values
        3. Validate and convert data types
        4. Remove invalid entries
        """
        print("\n🧹 Cleaning data...")
        self.df = self.raw_df.copy()
        
        # Remove duplicates
        duplicates_before = len(self.df)
        self.df = self.df.drop_duplicates()
        print(f"   Removed {duplicates_before - len(self.df)} duplicate rows")
        
        # Drop rows with missing critical values
        critical_cols = ["order_id", "customer_id", "order_amount"]
        rows_before = len(self.df)
        self.df = self.df.dropna(subset=critical_cols)
        print(f"   Removed {rows_before - len(self.df)} rows with missing critical values")
        
        # Fill missing values strategically
        if "product_name" in self.df.columns:
            self.df["product_name"].fillna("Unknown", inplace=True)
        if "product_category" in self.df.columns:
            self.df["product_category"].fillna("Other", inplace=True)
        
        # Convert order_date to datetime
        if "order_date" in self.df.columns:
            self.df["order_date"] = pd.to_datetime(self.df["order_date"], errors="coerce")
        
        # Convert order_amount to float
        if "order_amount" in self.df.columns:
            self.df["order_amount"] = self.df["order_amount"].astype(float, errors="ignore")
        
        # Validate order_amount is non-negative
        self.df = self.df[self.df["order_amount"] >= 0]
        
        # Standardize status values
        if "status" in self.df.columns:
            self.df["status"] = self.df["status"].str.lower().str.strip()
            valid_statuses = {"completed", "cancelled", "pending"}
            self.df = self.df[self.df["status"].isin(valid_statuses)]
        
        print(f"   ✅ Cleaned data: {len(self.df)} rows remaining")
        return self.df
    
    def build_domain_objects(self) -> None:
        """
        Convert DataFrame rows into domain objects (Product, Customer, Order).
        
        Demonstrates:
        - Object instantiation from data
        - OOP validation during construction
        - Building domain models from raw data
        """
        if self.df is None:
            raise ValueError("Data must be cleaned before building objects")
        
        print("\n🏗️ Building domain objects from data...")
        
        # Build unique products from the dataset
        for _, row in self.df[["product_name", "product_category", "unit_price"]].drop_duplicates().iterrows():
            product = self._build_product_from_row(row["product_name"], row["product_category"], row["unit_price"])
            if product:
                self.products[product.id] = product
        print(f"   Created {len(self.products)} Product objects")
        
        # Build customers with computed lifetime value
        for customer_id in self.df["customer_id"].unique():
            customer_orders = self.df[self.df["customer_id"] == customer_id]
            customer = self._build_customer_from_id(customer_id, customer_orders)
            if customer:
                self.customers[customer.id] = customer
        print(f"   Created {len(self.customers)} Customer objects")
        
        # Build orders with validation
        for _, row in self.df.iterrows():
            order = self._build_order_from_row(row)
            if order:
                self.orders.append(order)
        print(f"   Created {len(self.orders)} Order objects")
        print(f"   ✅ Domain objects ready for analysis")
    
    def export_clean_data(self, output_path: str = "output/sales_clean.csv") -> None:
        """Export cleaned dataset to CSV"""
        if self.df is None:
            raise ValueError("Data must be cleaned before export")
        self.df.to_csv(output_path, index=False)
        print(f"   Exported to {output_path}")
    
    # ========================================================================
    # BUSINESS ANALYTICS - Answer Key Questions
    # ========================================================================
    
    def get_analytics(self) -> dict:
        """Generate all key business metrics"""
        if self.df is None:
            raise ValueError("Data must be cleaned first")
        
        analytics = {}
        
        # 1. Total Revenue & Average Order Value
        analytics["total_revenue"] = self.df["order_amount"].sum()
        analytics["avg_order_value"] = self.df["order_amount"].mean()
        analytics["customer_count"] = self.df["customer_id"].nunique()
        analytics["order_count"] = len(self.df)
        
        # 2. Revenue by Category
        analytics["revenue_by_category"] = self.df.groupby("product_category")["order_amount"].sum().to_dict()
        
        # 3. Top 10 Customers by Lifetime Value
        customer_ltv = self.df.groupby("customer_id")["order_amount"].sum().sort_values(ascending=False)
        analytics["top_10_customers"] = customer_ltv.head(10).to_dict()
        
        # 4. Order Status Distribution
        analytics["order_status_dist"] = self.df["status"].value_counts().to_dict()
        
        # 5. Average Order Value by Category
        analytics["avg_order_by_category"] = self.df.groupby("product_category")["order_amount"].mean().to_dict()
        
        # 6. Repeat Customer Rate
        total_customers = self.df["customer_id"].nunique()
        repeat_purchases = self.df.groupby("customer_id").size()
        repeat_customers = (repeat_purchases > 1).sum()
        analytics["repeat_customer_rate"] = (repeat_customers / total_customers * 100) if total_customers > 0 else 0
        
        # 7. Monthly Revenue Trends
        if "order_date" in self.df.columns:
            monthly_revenue = self.df.groupby(self.df["order_date"].dt.to_period("M"))["order_amount"].sum()
            analytics["monthly_revenue"] = monthly_revenue.to_dict()
        
        # 8. Order Value Outliers (using IQR method)
        Q1 = self.df["order_amount"].quantile(0.25)
        Q3 = self.df["order_amount"].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = self.df[(self.df["order_amount"] < lower_bound) | (self.df["order_amount"] > upper_bound)]
        analytics["outlier_count"] = len(outliers)
        analytics["outlier_percentage"] = (len(outliers) / len(self.df) * 100)
        
        return analytics
    
    def analyze_with_objects(self) -> Dict:
        """
        Demonstrate OOP usage: analyze using domain objects.
        
        Shows students how to work with model instances to extract insights.
        Importantly, demonstrates POLYMORPHISM: the same method (get_discount_rate)
        produces different results based on customer type, without needing if/elif.
        """
        if not self.customers or not self.products:
            raise ValueError("Domain objects must be built first")
        
        print("\n🎯 OOP Analysis with Polymorphism:")
        
        # Find top customer using Customer objects
        top_customer = max(self.customers.values(), 
                          key=lambda c: c.lifetime_value)
        print(f"   Top Customer (OOP): {top_customer}")
        print(f"      → Type: {type(top_customer).__name__}")
        print(f"      → Discount Rate: {top_customer.get_discount_rate()*100:.1f}%")
        
        # Find most expensive product using Product objects
        most_expensive = max(self.products.values(), 
                            key=lambda p: p.base_price)
        print(f"\n   Most Expensive Product (OOP): {most_expensive}")
        print(f"      → Price for 1 unit: ${most_expensive.get_price(1):,.2f}")
        print(f"      → Price for 10 units: ${most_expensive.get_price(10):,.2f}")
        
        # Demonstrate polymorphism: different customer types, different discounts
        print(f"\n   💫 POLYMORPHISM: Same interface, different behavior:")
        print(f"      Testing $1,000 order with different customer types:")
        
        sample_customers = list(self.customers.values())[:5]  # Sample 5 customers
        for customer in sample_customers:
            discounted = customer.apply_discount(1000)
            saved = 1000 - discounted
            print(f"      {customer.__class__.__name__:20} → ${discounted:,.2f} (saved ${saved:,.2f})")
        
        # Count orders by status using Order objects
        status_counts = {}
        for order in self.orders:
            status_counts[order.status] = status_counts.get(order.status, 0) + 1
        
        print(f"\n   Order Status Distribution (using Order objects):")
        for status, count in status_counts.items():
            pct = (count / len(self.orders) * 100)
            print(f"      {status.title()}: {count} ({pct:.1f}%)")
        
        # Analyze customer tier distribution
        tier_counts = {}
        for customer in self.customers.values():
            tier = type(customer).__name__
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        print(f"\n   Customer Tier Distribution (Inheritance Hierarchy):")
        for tier, count in tier_counts.items():
            pct = (count / len(self.customers) * 100) if self.customers else 0
            print(f"      {tier}: {count} ({pct:.1f}%)")
        
        return {
            "top_customer": top_customer,
            "most_expensive_product": most_expensive,
            "status_counts": status_counts,
            "tier_distribution": tier_counts
        }

    
    def print_analytics_report(self) -> None:
        """Print formatted analytics report"""
        analytics = self.get_analytics()
        
        print("\n" + "="*60)
        print("📊 SALES ANALYTICS REPORT")
        print("="*60)
        print(f"Total Revenue: ${analytics['total_revenue']:,.2f}")
        print(f"Avg Order Value: ${analytics['avg_order_value']:,.2f}")
        print(f"Total Customers: {analytics['customer_count']}")
        print(f"Total Orders: {analytics['order_count']}")
        print(f"Repeat Customer Rate: {analytics['repeat_customer_rate']:.1f}%")
        print(f"Outlier Orders: {analytics['outlier_count']} ({analytics['outlier_percentage']:.1f}%)")
        
        print(f"\n💰 Revenue by Category:")
        for cat, rev in sorted(analytics['revenue_by_category'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {cat}: ${rev:,.2f}")
        
        print(f"\n🏆 Top 10 Customers (Lifetime Value):")
        for i, (cust, ltv) in enumerate(list(analytics['top_10_customers'].items())[:10], 1):
            print(f"   {i}. Customer {cust}: ${ltv:,.2f}")
        
        print(f"\n📈 Order Status Distribution:")
        for status, count in analytics['order_status_dist'].items():
            pct = (count / analytics['order_count'] * 100)
            print(f"   {status.title()}: {count} ({pct:.1f}%)")
        
        print("\n" + "="*60)
        
        return analytics
