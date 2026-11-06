
from db import get_connection 


def create_task_record(
    user_id: int,
    title: str,
    description: str,
    completed: bool
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks
                    (user_id, title, description, completed)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, title, description, completed)
            )

            task_id = cursor.lastrowid  

            cursor.execute(
                """
                SELECT task_id, title, description,
                       completed, user_id
                FROM tasks
                WHERE task_id = %s
                """,
                (task_id,)   
            )

            task = cursor.fetchone() 

        connection.commit()
        return task

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_all_task_records():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id, title, description,
                       completed, user_id
                FROM tasks
                ORDER BY task_id
                """
            )

            return cursor.fetchall() 

    finally:
        connection.close()


def get_user_task_records(user_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id, title, description,
                       completed, user_id
                FROM tasks
                WHERE user_id = %s                    
                ORDER BY task_id
                """,
                (user_id,)
            )

            return cursor.fetchall()  

    finally:
        connection.close()


def get_task_record(user_id: int, task_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id, title, description,
                       completed, user_id
                FROM tasks
                WHERE task_id = %s AND user_id = %s
                """,
                (task_id, user_id)
            )

            return cursor.fetchone()

    finally:
        connection.close()


def replace_task_record(
    user_id: int,
    task_id: int,
    title: str,
    description: str,
    completed: bool
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks
                SET title = %s,
                    description = %s,
                    completed = %s
                WHERE task_id = %s AND user_id = %s
                """,
                (title, description, completed, task_id, user_id)
            )

            if cursor.rowcount == 0:
                cursor.execute(
                    """
                    SELECT task_id
                    FROM tasks
                    WHERE task_id = %s AND user_id = %s
                    """,
                    (task_id, user_id)
                )

                if cursor.fetchone() is None:
                    return None

            cursor.execute(
                """
                SELECT task_id, title, description,
                       completed, user_id
                FROM tasks
                WHERE task_id = %s AND user_id = %s
                """,
                (task_id, user_id)
            )

            task = cursor.fetchone()

        connection.commit()
        return task

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def patch_task_record(
    user_id: int,
    task_id: int,
    updates: dict
):
    allowed_fields = {"title", "description", "completed"}

    updates = {
        field: value
        for field, value in updates.items()
        if field in allowed_fields and value is not None
    }

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id
                FROM tasks
                WHERE task_id = %s AND user_id = %s
                """,
                (task_id, user_id)
            )

            if cursor.fetchone() is None:
                return None

            if updates:
                set_parts = [
                    f"{field} = %s" for field in updates
                ]

                values = list(updates.values())
                values.extend([task_id, user_id])

                query = f"""
                    UPDATE tasks
                    SET {", ".join(set_parts)}
                    WHERE task_id = %s AND user_id = %s
                """

                cursor.execute(query, tuple(values))

            cursor.execute(
                """
                SELECT task_id, title, description,
                       completed, user_id
                FROM tasks
                WHERE task_id = %s AND user_id = %s
                """,
                (task_id, user_id)
            )

            task = cursor.fetchone()

        connection.commit()
        return task

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def delete_task_record(user_id: int, task_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT task_id, title, description,
                       completed, user_id
                FROM tasks
                WHERE task_id = %s AND user_id = %s
                """,
                (task_id, user_id)
            )

            task = cursor.fetchone()

            if task is None:
                return None

            cursor.execute(
                """
                DELETE FROM tasks
                WHERE task_id = %s AND user_id = %s
                """,
                (task_id, user_id)
            )

        connection.commit()
        return task

    except Exception:
        connection.rollback()
        raise
    
    finally:
        connection.close()
