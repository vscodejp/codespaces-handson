from typing import cast
from mysql.connector.pooling import MySQLConnectionPool
from flask import Flask, render_template, request

app = Flask(
    __name__,
    static_url_path="",
    static_folder="../public",
    template_folder="../public",
)

pool = MySQLConnectionPool(host="mysql", user="root", database="main")


# index.html
@app.route("/")
def index():
    return render_template("index.html")


# 未完了のタスクの一覧を表示する
# GET /api/tasks
#
# レスポンスBODY: 未完了のタスク型の配列のJSON
# 例:
# [
#   {
#     "id": 2,
#     "content": "VS Code に Python 拡張機能のインストール",
#     "completed": false
#   },
#   {
#     "id": 3,
#     "content": "GitHub Codespaces の体験 ",
#     "completed": false
#   }
# ]
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
                # (id, "タスクの内容", false) の形のタプルとしてとれる
                # JSON に変換できるように、dict 型にする
                records.append(
                    {
                        "id": record_tuple[0],
                        "content": record_tuple[1],
                        "completed": record_tuple[2] == 1,
                    }
                )

    # dict 型の配列を返す
    return records


# タスクを登録する
# POST /api/tasks
#
# リクエストBODY: 1 つのタスクを示すJSON。ただし、idと、completedは未入力。
# 例:
# {"content": "VS Code の 更新"}
#
# レスポンスBODY: 登録された1つのタスクを示すJSON
# 例:
# {
#    "id": 4,
#    "content": "VS Code の 更新",
#    "completed": false
# }
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

            # DB で INSERT クエリで振られる id
            new_id = cursor.lastrowid
        conn.commit()

    # 登録できたタスクの内容を返す
    return {
        "id": new_id,
        "content": content,
        "completed": False,
    }


# タスクを完了にする
# POST /api/tasks/<タスクのID>/done
#
# リクエストBODY: なし
#
# レスポンスBODY: 登録された1つのタスクを示すJSON
# 例:
# {
#   "id": 3,
#   "content": "GitHub Codespaces の体験 ",
#   "completed": true
# }
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
