#!/bin/env python
# 環境初期化スクリプト
import os
import sys
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
    run(["env", "python", "-m", "venv", venv_path])

    # 依存スクリプトの実行
    run(["env", "poetry", "install"])

    # vnv 内での実行に切り替え
    run(["poetry", "run", path.join(".", "initialize.py")])

    sys.exit(0)

wait_mysql_started()

run(["mysql", "-h", "mysql", "-u", "root", "main", "-e", "source ./database/ddl.sql"])

run(["mysql", "-h", "mysql", "-u", "root", "main", "-e", "source ./database/data.sql"])