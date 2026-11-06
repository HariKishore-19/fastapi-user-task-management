
from db import get_connection


def create_user_record(name: str, email: str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (name, email)
                VALUES (%s, %s)
                """,
                (name, email)
            )

            user_id = cursor.lastrowid

            cursor.execute(
                """
                SELECT user_id, name, email, created_at
                FROM users
                WHERE user_id = %s
                """,
                (user_id,)                   
               
            )

            user = cursor.fetchone()

        connection.commit()
        return user

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_user_record(user_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT user_id, name, email, created_at
                FROM users
                WHERE user_id = %s
                """,
                (user_id,)
            )

            user = cursor.fetchone()

        return user

    finally:
        connection.close()
