import mysql.connector

def connect_to_prodev():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="ALX_prodev"
    )

def stream_user_ages():
    conn = connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    conn.close()

def calculate_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():  # Loop 1
        total += age
        count += 1
    average = total / count if count else 0
    print(f"Average age of users: {average:.2f}")

# Run the function
if __name__ == "__main__":
    calculate_average_age()
