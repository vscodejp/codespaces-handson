#!/bin/env python
# 環境初期化スクリプト
import os
from os import path
import subprocess
import time


def run(cmd: list[str]):
    """ コマンド実行時スニペット """
    print("\033[1m" + " ".join(cmd) + "\033[0m")
    subprocess.run(cmd, check=True)


def wait_mysql_started():
    """ mysql の起動まで待機 """
    print("wait mysql start", end="")
    while True:
        print(".", end="")
        result = subprocess.run(["mysql", "-h", "mysql", "-u", "root", "-e", "SHOW DATABASES;"], check=False, capture_output=True)
        if result.returncode > 0:
            time.sleep(1)
            continue
        if str(result.stdout).count("main") > 0:
            break
        time.sleep(1)
    print()

venv_path = path.join(os.getcwd(), ".venv")
if not path.exists(venv_path):
    # venv がない場合は作る
    run(["python", "-m", "venv", venv_path])

# 依存パッケージの読み込み
run(["poetry", "install"])
run(["npm", "install"])


# MySQL が起動するまで待機
wait_mysql_started()

# DB の初期化
run(["mysql", "-h", "mysql", "-u", "root", "main", "-e", "source ./database/ddl.sql"])
run(["mysql", "-h", "mysql", "-u", "root", "main", "-e", "source ./database/data.sql"])
