import pandas as pd

# Đọc dữ liệu từ file
df = pd.read_csv('tmdb-movies.csv')

# Tìm đạo diễn có nhiều bộ phim nhất
top_director = df['director'].value_counts().idxmax()
num_movies_directed = df['director'].value_counts().max()

# Tìm diễn viên đóng nhiều phim nhất
# Bóc tách danh sách diễn viên, sau đó đếm số lần xuất hiện của mỗi diễn viên
actors_series = df['cast'].dropna().str.split(',').explode().str.strip()
top_actor = actors_series.value_counts().idxmax()
num_movies_acted = actors_series.value_counts().max()

# Hiển thị kết quả
print(f"Đạo diễn có nhiều bộ phim nhất: {top_director} ({num_movies_directed} phim)")
print(f"Diễn viên đóng nhiều phim nhất: {top_actor} ({num_movies_acted} phim)")
