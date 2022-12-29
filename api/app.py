from typing import cast
from mysql.connector.pooling import MySQLConnectionPool
from flask import Flask, render_template, request

app = Flask(
    __name__,
    static_url_path="",
    static_folder="../html",
    template_folder="../html",
)

pool = MySQLConnectionPool(host="mysql", user="root", database="main")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def show_remained_tasks():
    records = []
    with pool.get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
                SELECT
                    id,
                    content,
                    completed
                FROM tasks
                WHERE
                    completed = 0
            """
            cursor.execute(sql)
            for record_tuple in cursor:
                records.append(
                    {
                        "id": record_tuple[0],
                        "content": record_tuple[1],
                        "completed": record_tuple[2] == 1,
                    }
                )
    return records


@app.route("/api/tasks", methods=["POST"])
def append_task():
    request_param = cast(dict, request.get_json())
    with pool.get_connection() as conn:
        with conn.cursor() as cursor:
            content = request_param["content"]
            sql = """
                INSERT INTO tasks
                (
                    content,
                    completed
                )
                VALUES
                (
                    %s,
                    %s
                )
            """
            cursor.execute(sql, (content, False))
            new_id = cursor.lastrowid
        conn.commit()
    return {
        "id": new_id,
        "content": content,
        "completed": False,
    }


@app.route("/api/tasks/<int:task_id>/done", methods=["POST"])
def done_task(task_id: int):
    with pool.get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
                SELECT
                    id,
                    content,
                    completed
                FROM tasks
                WHERE
                    completed = 0
                    AND id = %s
            """
            cursor.execute(sql, [task_id])
            record_tuple = cursor.fetchone()
            if cursor.rowcount == 0:
                return {}, 404

        with conn.cursor() as cursor:
            sql = f"""
                UPDATE tasks
                SET
                    completed = 1
                WHERE
                    id = %s
            """
            cursor.execute(sql, [task_id])
        conn.commit()
    return {
        "id": task_id,
        "content": record_tuple[1],
        "completed": True,
    }


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
