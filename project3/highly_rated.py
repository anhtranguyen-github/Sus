import pandas as pd

# Đọc dữ liệu từ file
df = pd.read_csv('tmdb-movies.csv')

# Lọc các bộ phim có vote_average > 7.5
highly_rated_movies = df[df['vote_average'] > 7.5]

# Lưu kết quả vào file mới
highly_rated_movies.to_csv('highly_rated_movies.csv', index=False)

print("Đã lưu các bộ phim có đánh giá trung bình trên 7.5 vào 'highly_rated_movies.csv'.")
