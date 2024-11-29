import psycopg2
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("query.log"),
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

# Query to count the number of rows in the `products` table
try:
    cursor.execute("SELECT COUNT(*) FROM products;")
    result = cursor.fetchone()
    logging.info(f"Number of rows in the 'products' table: {result[0]}")
except Exception as e:
    logging.error(f"Failed to execute query: {e}")

# Close the database connection
cursor.close()
conn.close()
logging.info("Database connection closed.")
