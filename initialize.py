#!/bin/env python
# 環境初期化スクリプト
import os
import sys
from os import path
import subprocess


def run_cmd(command: list[str]):
    print("\033[1m" + " ".join(command) + "\033[0m")
    subprocess.run(command, check=True)

venv_path = path.join(os.getcwd(), ".venv")
if not path.exists(venv_path):
    # venv がない場合は作る
    run_cmd(["env", "python", "-m", "venv", venv_path])

    # 依存スクリプトの実行
    run_cmd(["env", "poetry", "install"])

    # vnv 内での実行に切り替え
    run_cmd(["poetry", "run", path.join(".", "initialize.py")])

    sys.exit(0)

run_cmd(["mysql", "-h", "mysql", "main", "-e", "source ./database/ddl.sql"])