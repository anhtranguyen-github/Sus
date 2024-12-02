import pandas as pd

# Đọc dữ liệu từ file
df = pd.read_csv('tmdb-movies.csv')

# Tính lợi nhuận cho mỗi bộ phim
df['profit'] = df['revenue'] - df['budget']

# Sắp xếp theo lợi nhuận giảm dần và lấy top 10
top_10_profitable_movies = df.sort_values(by='profit', ascending=False).head(10)

# Hiển thị kết quả ra màn hình
print("Top 10 bộ phim có lợi nhuận cao nhất:")
print(top_10_profitable_movies[['original_title', 'profit', 'revenue', 'budget']])
