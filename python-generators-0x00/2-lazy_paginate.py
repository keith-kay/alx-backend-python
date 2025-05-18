import mysql.connector

def connect_to_prodev():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="ALX_prodev"
    )

def paginate_users(page_size, offset):
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def lazy_paginate(page_size):
    offset = 0
    while True:  # this is the only loop allowed
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
