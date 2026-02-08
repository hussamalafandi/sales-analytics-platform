from analyzer import load_data, clean_data, analyze_data

try:
    df = load_data('./data/sales_data.csv')
except FileNotFoundError:
    exit(1)

df = clean_data(df)
print(df.info())

print("Performing analysis...")
analytics = analyze_data(df)
print("\nAnalytics Results:")
for key, value in analytics.items():
    print(f"{key}: {value}")
