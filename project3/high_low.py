import pandas as pd

# Đọc dữ liệu từ file
df = pd.read_csv('tmdb-movies.csv')

# Tìm bộ phim có doanh thu cao nhất
highest_revenue_movie = df.loc[df['revenue'].idxmax()]

# Tìm bộ phim có doanh thu thấp nhất
lowest_revenue_movie = df.loc[df['revenue'].idxmin()]

print("Phim có doanh thu cao nhất:")
print(highest_revenue_movie["original_title"])

print("\nPhim có doanh thu thấp nhất:")
print(lowest_revenue_movie["original_title"])
