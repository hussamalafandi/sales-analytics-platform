"""
Utility Functions
Demonstrates: Helper functions, file I/O, and report generation
"""
import json
from datetime import datetime
from pathlib import Path


def create_output_directory(output_dir: str = "output") -> None:
    """Create output directory if it doesn't exist"""
    Path(output_dir).mkdir(exist_ok=True)


def save_report(analytics: dict, output_path: str = "output/summary_report.txt") -> None:
    """
    Save analytics report to text file
    
    Args:
        analytics: Dictionary of analytics metrics
        output_path: Path to save the report
    """
    create_output_directory()
    
    with open(output_path, "w") as f:
        f.write("="*70 + "\n")
        f.write("SALES ANALYTICS PLATFORM - SUMMARY REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        # Key Metrics
        f.write("KEY METRICS\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total Revenue: ${analytics['total_revenue']:,.2f}\n")
        f.write(f"Average Order Value: ${analytics['avg_order_value']:,.2f}\n")
        f.write(f"Total Customers: {analytics['customer_count']}\n")
        f.write(f"Total Orders: {analytics['order_count']}\n")
        f.write(f"Repeat Customer Rate: {analytics['repeat_customer_rate']:.1f}%\n")
        f.write(f"Outlier Orders: {analytics['outlier_count']} ({analytics['outlier_percentage']:.1f}%)\n\n")
        
        # Revenue by Category
        f.write("REVENUE BY CATEGORY\n")
        f.write("-" * 70 + "\n")
        for cat, rev in sorted(analytics['revenue_by_category'].items(), key=lambda x: x[1], reverse=True):
            f.write(f"{cat}: ${rev:,.2f}\n")
        f.write("\n")
        
        # Top 10 Customers
        f.write("TOP 10 CUSTOMERS (Lifetime Value)\n")
        f.write("-" * 70 + "\n")
        for i, (cust, ltv) in enumerate(list(analytics['top_10_customers'].items())[:10], 1):
            f.write(f"{i}. Customer {cust}: ${ltv:,.2f}\n")
        f.write("\n")
        
        # Order Status
        f.write("ORDER STATUS DISTRIBUTION\n")
        f.write("-" * 70 + "\n")
        for status, count in analytics['order_status_dist'].items():
            pct = (count / analytics['order_count'] * 100)
            f.write(f"{status.title()}: {count} ({pct:.1f}%)\n")
        f.write("\n")
    
    print(f"✅ Report saved to {output_path}")


def save_algorithm_comparison(sorting_results: dict, searching_results: dict, 
                            output_path: str = "output/algorithm_comparison.txt") -> None:
    """
    Save algorithm performance comparison report
    
    Args:
        sorting_results: Dictionary of sorting algorithm times
        searching_results: Dictionary of searching algorithm times
        output_path: Path to save the report
    """
    create_output_directory()
    
    with open(output_path, "w") as f:
        f.write("="*70 + "\n")
        f.write("ALGORITHM PERFORMANCE ANALYSIS\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        f.write("SORTING ALGORITHM COMPARISON\n")
        f.write("-" * 70 + "\n")
        f.write("Algorithm\t\tExecution Time (seconds)\tComplexity\n")
        f.write("-" * 70 + "\n")
        
        complexities = {
            "Bubble Sort": "O(n²)",
            "Merge Sort": "O(n log n)",
            "Python sorted()": "O(n log n) - Timsort"
        }
        
        for algo, time in sorted(sorting_results.items(), key=lambda x: x[1]):
            complexity = complexities.get(algo, "—")
            f.write(f"{algo:<20}\t{time:.6f}\t\t\t{complexity}\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("SEARCHING ALGORITHM COMPARISON\n")
        f.write("-" * 70 + "\n")
        f.write("Algorithm\t\tExecution Time (seconds)\tComplexity\n")
        f.write("-" * 70 + "\n")
        
        search_complexities = {
            "Linear Search": "O(n)",
            "Binary Search": "O(log n)",
            "'in' operator": "O(n) - optimized in C"
        }
        
        for algo, time in sorted(searching_results.items(), key=lambda x: x[1]):
            complexity = search_complexities.get(algo, "—")
            f.write(f"{algo:<20}\t{time:.6f}\t\t\t{complexity}\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("INSIGHTS\n")
        f.write("-" * 70 + "\n")
        f.write("• Built-in functions are typically faster due to optimized C implementations\n")
        f.write("• Merge Sort (O(n log n)) outperforms Bubble Sort (O(n²)) on large datasets\n")
        f.write("• Binary Search is much faster than Linear Search on sorted data\n")
        f.write("• Always use appropriate algorithms for your use case\n")
    
    print(f"✅ Algorithm comparison saved to {output_path}")
