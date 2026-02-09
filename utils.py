import os
import matplotlib.pyplot as plt
from analyzer import DataAnalyzer

def create_output_directory():
    """Create output directory if it doesn't exist"""
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def create_visualizations(analyzer: DataAnalyzer, analytics: dict) -> None:
    """Create and save visualizations"""
    create_output_directory()

    if analyzer.df is None:
        print("No data available for visualization.")
        return
    
    print("\n📊 Creating visualizations...")
    
    # Set style
    plt.style.use("seaborn-v0_8-darkgrid")
    
    # ========================================================================
    # 1. BAR CHART: Revenue by Category
    # ========================================================================
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = list(analytics["revenue_by_category"].keys())
    revenues = list(analytics["revenue_by_category"].values())
    
    bars = ax.bar(categories, revenues, color="#2E86AB", edgecolor="black", alpha=0.8)
    ax.set_xlabel("Product Category", fontsize=12, fontweight="bold")
    ax.set_ylabel("Revenue ($)", fontsize=12, fontweight="bold")
    ax.set_title("Revenue by Product Category", fontsize=14, fontweight="bold")
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}',
                ha='center', va='bottom', fontsize=10)
    
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("output/revenue_by_category.png", dpi=300, bbox_inches="tight")
    print("   ✅ Saved: revenue_by_category.png")
    plt.close()
    
    # ========================================================================
    # 2. LINE CHART: Monthly Revenue Trend
    # ========================================================================
    if "monthly_revenue" in analytics and analytics["monthly_revenue"]:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        months = list(analytics["monthly_revenue"].keys())
        revenues_monthly = list(analytics["monthly_revenue"].values())
        
        # Convert month objects to strings if necessary
        months_str = [str(m) for m in months]
        
        ax.plot(months_str, revenues_monthly, marker="o", linewidth=2, 
                markersize=8, color="#A23B72", markerfacecolor="#F18F01")
        ax.fill_between(range(len(months_str)), revenues_monthly, alpha=0.3, color="#A23B72")
        
        ax.set_xlabel("Month", fontsize=12, fontweight="bold")
        ax.set_ylabel("Revenue ($)", fontsize=12, fontweight="bold")
        ax.set_title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
        
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig("output/monthly_revenue_trend.png", dpi=300, bbox_inches="tight")
        print("   ✅ Saved: monthly_revenue_trend.png")
        plt.close()
    
    # ========================================================================
    # 3. HISTOGRAM: Order Value Distribution
    # ========================================================================
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(analyzer.df["order_amount"], bins=30, color="#06A77D", 
            edgecolor="black", alpha=0.8)
    ax.set_xlabel("Order Amount ($)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Frequency", fontsize=12, fontweight="bold")
    ax.set_title("Order Value Distribution", fontsize=14, fontweight="bold")
    
    # Add statistics
    mean_val = analyzer.df["order_amount"].mean()
    median_val = analyzer.df["order_amount"].median()
    ax.axvline(mean_val, color="red", linestyle="--", linewidth=2, label=f"Mean: ${mean_val:.2f}")
    ax.axvline(median_val, color="green", linestyle="--", linewidth=2, label=f"Median: ${median_val:.2f}")
    ax.legend()
    
    plt.tight_layout()
    plt.savefig("output/order_distribution.png", dpi=300, bbox_inches="tight")
    print("   ✅ Saved: order_distribution.png")
    plt.close()
    
    # ========================================================================
    # 4. BONUS: Pie Chart - Order Status Distribution
    # ========================================================================
    fig, ax = plt.subplots(figsize=(8, 8))
    
    statuses = list(analytics["order_status_distribution"].keys())
    counts = list(analytics["order_status_distribution"].values())
    colors = ["#06A77D", "#D62828", "#F77F00"]
    
    ax.pie(counts, labels=statuses, autopct="%1.1f%%", startangle=90,
           colors=colors[:len(statuses)], textprops={"fontsize": 11, "fontweight": "bold"})
    ax.set_title("Order Status Distribution", fontsize=14, fontweight="bold")
    
    plt.tight_layout()
    plt.savefig("output/order_status_distribution.png", dpi=300, bbox_inches="tight")
    print("   ✅ Saved: order_status_distribution.png")
    plt.close()
    