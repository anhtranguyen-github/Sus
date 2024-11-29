import os
import json
import psycopg2
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_insertion.log"),
        logging.StreamHandler()
    ]
)

# Database connection parameters
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="new_user",
        password="1",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    logging.info("Database connection established.")
except Exception as e:
    logging.error(f"Failed to connect to the database: {e}")
    exit()

# Directory containing JSON files
json_dir = '../project2/tiki_product_data'

# Loop through each JSON file and insert data
for filename in sorted(os.listdir(json_dir)):
    if filename.endswith('.json'):
        file_path = os.path.join(json_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logging.info(f"Loaded data from {filename} successfully.")
            
            # Insert data into the database
            for item in data:
                try:
                    cursor.execute("""
                        INSERT INTO products (id, name, url_key, price, description, images)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """, (
                        item['id'],
                        item['name'],
                        item['url_key'],
                        item['price'],
                        item['description'],
                        item['images']
                    ))
                    logging.info(f"Inserted product ID {item['id']} from {filename} successfully.")
                except psycopg2.IntegrityError as e:
                    conn.rollback()  # Roll back the current transaction after an error
                    logging.error(f"Integrity error for product ID {item['id']} from {filename}: {e}")
                except Exception as e:
                    logging.error(f"Failed to insert product ID {item['id']} from {filename}: {e}")

        except Exception as e:
            logging.error(f"Failed to load data from {filename}: {e}")

# Commit changes and close the connection
try:
    conn.commit()
    logging.info("Transaction committed successfully.")
except Exception as e:
    logging.error(f"Failed to commit transaction: {e}")

cursor.close()
conn.close()
logging.info("Database connection closed.")
