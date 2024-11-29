import csv
import requests
import json
import os
import logging
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# File paths and output configuration
input_file = 'products-0-200000(in).csv'
output_folder = 'tiki_product_data'
error_file = 'tiki_product_errors.json'
log_file = 'tiki_product_log.log'
batch_size = 1000

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Setup requests session with retry logic
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

# Read product IDs from CSV
def read_product_ids(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return [row[0] for row in reader]

# Clean HTML content from description
def clean_description(description):
    if not description:
        return None
    soup = BeautifulSoup(description, "html.parser")
    text = soup.get_text()
    return ' '.join(text.split())

# Fetch product data from API
def fetch_product_data(product_id):
    url = f"https://api.tiki.vn/product-detail/api/v1/products/{product_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Connection": "keep-alive",
    }
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        product_data = response.json()
        return {
            "id": product_data.get("id"),
            "name": product_data.get("name"),
            "url_key": product_data.get("url_key"),
            "price": product_data.get("price"),
            "description": clean_description(product_data.get("description")),
            "images": [img.get("large_url") for img in product_data.get("images", [])],
        }
    except Exception as e:
        logging.error(f"Error fetching product {product_id}: {e}")
        return {"error": str(e), "id": product_id}

# Process batch with concurrent requests
def process_batch_concurrently(batch):
    results = []
    errors = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(fetch_product_data, pid): pid for pid in batch}
        for future in as_completed(future_to_id):
            try:
                data = future.result()
                if "error" in data:
                    errors.append(data)
                else:
                    results.append(data)
            except Exception as exc:
                errors.append({"error": str(exc), "id": future_to_id[future]})
                logging.error(f"Unexpected error: {exc}")
    return results, errors

# Process each batch and save results
def process_batch(batch, batch_index):
    batch_data, errors = process_batch_concurrently(batch)

    # Save batch data
    output_file = os.path.join(output_folder, f"products_batch_{batch_index}.json")
    with open(output_file, mode='w', encoding='utf-8') as file:
        json.dump(batch_data, file, ensure_ascii=False, indent=4)
    logging.info(f"Saved batch {batch_index} with {len(batch_data)} products.")

    # Save errors
    if errors:
        with open(error_file, mode='a', encoding='utf-8') as file:
            json.dump(errors, file, ensure_ascii=False, indent=4)
        logging.info(f"Logged {len(errors)} errors for batch {batch_index}.")

# Main function
def main():
    product_ids = read_product_ids(input_file)
    total_batches = (len(product_ids) + batch_size - 1) // batch_size

    for i in range(total_batches):
        start = i * batch_size
        end = start + batch_size
        batch = product_ids[start:end]
        logging.info(f"Processing batch {i + 1}/{total_batches}...")
        process_batch(batch, i + 1)

if __name__ == "__main__":
    main()
