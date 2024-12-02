import pandas as pd

# Đọc dữ liệu từ file
df = pd.read_csv('tmdb-movies.csv')

# Tách các thể loại, loại bỏ giá trị NaN và đếm số lần xuất hiện của mỗi thể loại
genres_series = df['genres'].dropna().str.split('|').explode().str.strip()
genre_counts = genres_series.value_counts()

# Hiển thị kết quả
print("Thống kê số lượng phim theo thể loại:")
print(genre_counts)
