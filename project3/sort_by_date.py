import pandas as pd

# Đọc dữ liệu từ file
df = pd.read_csv('tmdb-movies.csv')

# Chuyển đổi cột 'release_date' thành kiểu datetime với format MM/DD/YY
df['release_date'] = pd.to_datetime(df['release_date'], format='%m/%d/%y', errors='coerce')

# Sử dụng cột 'release_year' để thay đổi năm trong 'release_date'
df['release_date'] = df.apply(
    lambda row: row['release_date'].replace(year=row['release_year']) if pd.notnull(row['release_date']) else row['release_date'],
    axis=1
)

# Sắp xếp theo ngày phát hành giảm dần
sorted_df = df.sort_values(by='release_date', ascending=False)

# Quay lại định dạng cũ (MM/DD/YY)
sorted_df['release_date'] = sorted_df['release_date'].dt.strftime('%m/%d/%y')

# Lưu vào file mới
sorted_df.to_csv('tmdb-movies-sorted.csv', index=False)

print("Đã lưu file sắp xếp theo ngày phát hành vào 'tmdb-movies-sorted.csv'.")
