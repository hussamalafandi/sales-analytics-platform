from analyzer import load_data, clean_data

try:
    df = load_data('./data/sales_data.csv')
except FileNotFoundError:
    exit(1)

df = clean_data(df)
print(df.info())
