from analyzer import DataAnalyzer
from utils import create_visualizations

def main():
    # Create an instance of DataAnalyzer
    analyzer = DataAnalyzer()
    
    # Load data from CSV file
    file_path = './data/sales_data.csv'  # Update with your actual file path
    try:
        df = analyzer.load_data(file_path)
        print("Data loaded successfully.")
    except FileNotFoundError:
        return
    
    # Clean the data
    cleaned_df = analyzer.clean_data()
    print("Data cleaned successfully.")
    
    # Analyze the data and compute metrics
    metrics = analyzer.analyze_data()
    print("Data analysis completed. Key metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    # Print analytized data
    print("\nAnalytized Data:")
    analyzer.print_analytics()

    # Create and save visualizations
    create_visualizations(analyzer, metrics)

if __name__ == "__main__":
    main()
