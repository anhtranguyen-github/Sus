import requests

# URL API từ Postman
url = "https://api.tiki.vn/product-detail/api/v1/products/138083218"

# Headers lấy từ Postman
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Connection": "keep-alive",
}

try:
    # Gửi yêu cầu GET với headers
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Bắt lỗi HTTP nếu xảy ra

    # Lấy dữ liệu JSON
    product_data = response.json()

    # Trích xuất các thông tin cần thiết
    extracted_data = {
        "id": product_data.get("id"),
        "name": product_data.get("name"),
        "url_key": product_data.get("url_key"),
        "price": product_data.get("price"),
        "description": product_data.get("description"),
        "images": [image.get("large_url") for image in product_data.get("images", [])]
    }

    print("Thông tin trích xuất:")
    for key, value in extracted_data.items():
        print(f"{key}: {value}")

except requests.exceptions.RequestException as e:
    print(f"Lỗi xảy ra: {e}")
