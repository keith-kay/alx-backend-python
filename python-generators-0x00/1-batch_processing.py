import mysql.connector

def connect_to_prodev():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="ALX_prodev"
    )

def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) FROM user_data")
    total_rows = cursor.fetchone()["COUNT(*)"]

    for offset in range(0, total_rows, batch_size):
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if float(user['age']) > 25]
        for user in filtered:
            print(f"{user['name']} ({user['email']}), Age: {user['age']}")

