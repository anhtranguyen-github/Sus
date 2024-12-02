import pandas as pd

# Đọc dữ liệu từ file
df = pd.read_csv('tmdb-movies.csv')

# Tính tổng doanh thu
total_revenue = df['revenue'].sum()

print(f"Tổng doanh thu của tất cả các bộ phim: {total_revenue:,} USD")
