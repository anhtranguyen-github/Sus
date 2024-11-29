#!/bin/bash

echo "Đang tải dữ liệu từ https://raw.githubusercontent.com/yinghaoz1/tmdb-movie-dataset-analysis/master/tmdb-movies.csv"
curl -o tmdb-movies.csv https://raw.githubusercontent.com/yinghaoz1/tmdb-movie-dataset-analysis/master/tmdb-movies.csv

# 1. Sắp xếp các bộ phim theo ngày phát hành giảm dần rồi lưu ra một file mới
echo "Sắp xếp các bộ phim theo ngày phát hành giảm dần:"
csvsort -c release_date -r tmdb-movies.csv > sorted_by_date.csv
echo "Kết quả đã được lưu vào file sorted_by_date.csv"

# 2. Lọc ra các bộ phim có đánh giá trung bình trên 7.5 rồi lưu ra một file mới
echo "Lọc các bộ phim có đánh giá trung bình trên 7.5:"
csvgrep -c vote_average -r ^[78-9].[5-9] tmdb-movies.csv > movies_above_7.5.csv
echo "Kết quả đã được lưu vào file movies_above_7.5.csv"

# 3. Tìm ra phim nào có doanh thu cao nhất và doanh thu thấp nhất
echo "Doanh thu cao nhất và thấp nhất:"
echo "Doanh thu cao nhất:"
csvsort -c revenue -r tmdb-movies.csv | csvcut -c original_title,revenue | head -n 2
echo "Doanh thu thấp nhất:"
csvsort -c revenue tmdb-movies.csv | csvcut -c original_title,revenue | head -n 2

# 4. Tính tổng doanh thu tất cả các bộ phim
echo "Tổng doanh thu tất cả các bộ phim:"
awk -F, 'NR > 1 {sum += $5} END {print sum}' tmdb-movies.csv

# 5. Top 10 bộ phim đem về lợi nhuận cao nhất
echo "Top 10 bộ phim đem về lợi nhuận cao nhất:"
awk -F, 'NR > 1 {print $5, $6}' tmdb-movies.csv | sort -nr | head -n 10

# 6. Đạo diễn nào có nhiều bộ phim nhất và diễn viên nào đóng nhiều phim nhất
echo "Đạo diễn nào có nhiều bộ phim nhất:"
awk -F',' '{print $9}' tmdb-movies.csv | tail -n +2 | sort | uniq -c | sort -nr | sed -n '2p' | awk '{for(i=2;i<=NF;i++) printf "%s ", $i; print ""}'
echo "Diễn viên nào đóng nhiều phim nhất:"
awk -F',' '{print $7}' tmdb-movies.csv | tail -n +2 | tr '|' '\n' | sort | uniq -c | sort -nr | sed -n '2p' | awk '{for(i=2;i<=NF;i++) printf "%s ", $i; print ""}'
