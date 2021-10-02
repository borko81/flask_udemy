# import sqlite3

# connection = sqlite3.connect("data.db")
# cursor = connection.cursor()

# create_table = "CREATE TABLE IF NOT EXISTS users (id int, username text, password text )"
# cursor.execute(create_table)

# insert_query = "INSERT INTO users VALUES (?, ?, ?)"

# users = [
#     (1, "borko", "borko"),
#     (2, "test", "test")
# ]

# cursor.executemany(insert_query, users)

# select_query = cursor.execute("SELECT * FROM users")

# for user in select_query.fetchall():
#     print(user)

# connection.commit()
# connection.close()
