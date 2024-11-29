import csv
import requests
import json
import os
from bs4 import BeautifulSoup  # Thư viện để xử lý HTML

# File input chứa danh sách product IDs
input_file = 'products-0-200000(in).csv'
output_folder = 'tiki_product_data'
error_file = 'tiki_product_errors.json'

# Tạo thư mục lưu file nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

# Hàm đọc danh sách product IDs từ file CSV
def read_product_ids(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Bỏ qua tiêu đề
        return [row[0] for row in reader]

# Hàm chuẩn hóa nội dung của "description"
def clean_description(description):
    if not description:
        return None
    soup = BeautifulSoup(description, "html.parser")
    text = soup.get_text()  # Loại bỏ HTML tags
    return ' '.join(text.split())  # Loại bỏ khoảng trắng dư thừa

# Hàm lấy thông tin sản phẩm từ API
def fetch_product_data(product_id):
    url = f"https://api.tiki.vn/product-detail/api/v1/products/{product_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Connection": "keep-alive",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        product_data = response.json()

        # Trích xuất các thông tin cần thiết
        return {
            "id": product_data.get("id"),
            "name": product_data.get("name"),
            "url_key": product_data.get("url_key"),
            "price": product_data.get("price"),
            "description": clean_description(product_data.get("description")),
            "images": [img.get("large_url") for img in product_data.get("images", [])],
        }
    except Exception as e:
        return {"error": str(e), "id": product_id}

# Hàm xử lý một batch sản phẩm
def process_batch(batch, batch_index):
    batch_data = []
    errors = []

    for product_id in batch:
        product_data = fetch_product_data(product_id)

        # Phân loại kết quả (thành công hoặc lỗi)
        if "error" in product_data:
            errors.append(product_data)
        else:
            batch_data.append(product_data)

    # Lưu batch data vào file JSON
    output_file = os.path.join(output_folder, f"products_batch_{batch_index}.json")
    with open(output_file, mode='w', encoding='utf-8') as file:
        json.dump(batch_data, file, ensure_ascii=False, indent=4)
    print(f"Đã lưu batch {batch_index} với {len(batch_data)} sản phẩm.")

    # Lưu lỗi vào file errors.json
    if errors:
        with open(error_file, mode='a', encoding='utf-8') as file:
            json.dump(errors, file, ensure_ascii=False, indent=4)
        print(f"Đã ghi {len(errors)} sản phẩm lỗi vào '{error_file}'.")

# Hàm chính
def main():
    product_ids = read_product_ids(input_file)
    batch_size = 1000
    total_batches = (len(product_ids) + batch_size - 1) // batch_size

    for i in range(total_batches):
        start = i * batch_size
        end = start + batch_size
        batch = product_ids[start:end]
        print(f"Đang xử lý batch {i + 1}/{total_batches}...")
        process_batch(batch, i + 1)

if __name__ == "__main__":
    main()
