"""
Main Entry Point - Sales Analytics Platform
Orchestrates data loading, cleaning, analysis, and visualization
"""
import matplotlib.pyplot as plt
import pandas as pd
from analyzer import SalesAnalyzer
from algorithms import benchmark_sorting, benchmark_searching
from utils import create_output_directory, save_report, save_algorithm_comparison


def create_visualizations(analyzer: SalesAnalyzer, analytics: dict) -> None:
    """Create and save visualizations"""
    create_output_directory()
    
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
    
    statuses = list(analytics["order_status_dist"].keys())
    counts = list(analytics["order_status_dist"].values())
    colors = ["#06A77D", "#D62828", "#F77F00"]
    
    ax.pie(counts, labels=statuses, autopct="%1.1f%%", startangle=90,
           colors=colors[:len(statuses)], textprops={"fontsize": 11, "fontweight": "bold"})
    ax.set_title("Order Status Distribution", fontsize=14, fontweight="bold")
    
    plt.tight_layout()
    plt.savefig("output/order_status_distribution.png", dpi=300, bbox_inches="tight")
    print("   ✅ Saved: order_status_distribution.png")
    plt.close()


def run_algorithm_benchmarks(analyzer: SalesAnalyzer) -> None:
    """Run and report algorithm performance benchmarks"""
    print("\n⚡ Running algorithm benchmarks...")
    
    # Sorting benchmark
    sample_data = analyzer.df["order_amount"].head(100).tolist()
    sorting_results = benchmark_sorting(sample_data)
    
    print("\n   Sorting Algorithms (100 items):")
    for algo, time in sorted(sorting_results.items(), key=lambda x: x[1]):
        print(f"      {algo}: {time:.6f}s")
    
    # Searching benchmark
    search_target = analyzer.df["order_amount"].iloc[0]
    searching_results = benchmark_searching(sample_data, search_target)
    
    print("\n   Searching Algorithms (1000 iterations):")
    for algo, time in sorted(searching_results.items(), key=lambda x: x[1]):
        print(f"      {algo}: {time:.6f}s")
    
    # Save comparison report
    save_algorithm_comparison(sorting_results, searching_results)


def main():
    """Main orchestration function"""
    print("🚀 Sales Analytics Platform")
    print("="*60)
    
    # Initialize analyzer and load data
    try:
        analyzer = SalesAnalyzer("data/sales_data.csv")
        analyzer.load_data()
    except FileNotFoundError:
        print("❌ Error: data/sales_data.csv not found!")
        print("   Please ensure the data file exists or run the data generation script.")
        return
    
    # Clean data
    analyzer.clean_data()
    analyzer.export_clean_data()
    
    # Build and analyze with OOP domain objects
    analyzer.build_domain_objects()
    analyzer.analyze_with_objects()
    
    # Generate analytics
    analytics = analyzer.print_analytics_report()
    save_report(analytics)
    
    # Create visualizations
    create_visualizations(analyzer, analytics)
    
    # Run algorithm benchmarks
    run_algorithm_benchmarks(analyzer)
    
    print("\n" + "="*60)
    print("✅ Analysis complete! Check the 'output/' directory for results.")
    print("="*60)


if __name__ == "__main__":
    main()
