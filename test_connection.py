from db import get_connection

connection = None

try:
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE() AS db_name")
        result = cursor.fetchone()

        print("Connected database:", result["db_name"])
        print("PyMySQL connection is working!")

finally:
    if connection:
        connection.close()
