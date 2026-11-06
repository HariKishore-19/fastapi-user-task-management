
import pymysql


def get_connection():
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="todo_app_db",
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection
