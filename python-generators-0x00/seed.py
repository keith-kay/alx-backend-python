import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

DB_HOST = 'localhost'
DB_USER = 'root'  # change if needed
DB_PASSWORD = ''  # change if needed
DB_NAME = 'ALX_prodev'

def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )

def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
        print(f"Database '{DB_NAME}' ensured.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL,
        UNIQUE KEY email_unique (email)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    try:
        cursor.execute(create_table_query)
        print("Table 'user_data' ensured.")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
        exit(1)
    cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    # Check if email already exists to avoid duplicates
    select_query = "SELECT COUNT(*) FROM user_data WHERE email = %s"
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age) 
    VALUES (%s, %s, %s, %s)
    """
    for row in data:
        name, email, age = row
        cursor.execute(select_query, (email,))
        count = cursor.fetchone()[0]
        if count == 0:
            uid = str(uuid.uuid4())
            cursor.execute(insert_query, (uid, name, email, int(age)))
    connection.commit()
    cursor.close()
    print("Data inserted successfully.")

def read_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [(row['name'], row['email'], row['age']) for row in reader]
    return data

def main():
    # Connect to MySQL server (no DB selected yet)
    cnx = connect_db()
    create_database(cnx)
    cnx.close()

    # Connect to the created database
    cnx = connect_to_prodev()
    create_table(cnx)

    # Read CSV data
    data = read_csv('user_data.csv')

    # Insert data
    insert_data(cnx, data)

    cnx.close()
    print("Database seeded successfully.")

if __name__ == '__main__':
    main()
