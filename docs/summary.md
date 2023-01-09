## このコードのメインは 2 つ

- Python Web API のコード: [api/app.py](api/app.py)
- Frontend のコード: [api/app.py](api/app.py)
- Frontend のコードを使う HTML（これは演習中には編集しません）: [public/index.html](public/index.html)

## 完成したアプリでできること

- 未完了のタスクの一覧を表示する
- タスクを追加する
- タスクを完了にする

それぞれ、Web API では以下の URL で行えるようになっています。

- GET /api/tasks 未完了タスクを読み出す
- POST /api/tasks タスクを追加する
- POST /api/tasks/(id)/done id のタスクを完了にする

## 体験すること

### 拡張機能 MySQL を使って、DB の中身を確認する

アクティビティーバー（画面左のアイコン列）から、MySQL を選び「Create Connection」を押します。

以下を入力する（ほかは初期値のまま）

- ServerType: MySQL
- Name: mysql
- Host: mysql
- Database: main
- Username: root（初期値）
- Password: 空（初期値で空）

テーブル tasks の中身を、このツールで確認してみてください。

### Python の Web API をデバッグする

Python Web API のコード [api/app.py](api/app.py) を開きます。各 Web API の実装が確認できるようになっています。

この Web API を立ち上げるには、デバッグ設定「Launch Web API (Python Flask)」をデバッグ実行します。
この[デバッグ設定](.vscode/launch.json)は、api/app.py を起点にして Flask を立ち上げる設定になっています。

各 API にアクセスするには、拡張機能 REST Client を使います。

[REST Client の命令ファイル rest_client.http](rest_client.http) を開いて、各リクエストを実行できます。

api/app.py のコードにブレークポイントを置き、REST Client でアクセスするとブレークされることを確認してください。

### Frontend をデバッグする

Web Frontend のコード [frontend/main.ts](frontend/main.ts) を開きます。
ブラウザの操作で各関数が呼び出されて、Web API にアクセスして仕事をするようになっています。

Frontend は TypeScript で実装されており、コンパイルする必要があります。
コンパイルするには、タスク「Typescript Compile」を実行してください。
実行すると、コードの編集の度に自動でコンパイルされる watch モードでコンパイラが実行されています。

コンパイル後のコードは [public/js/main.js](public/js/main.js) に出力されています。 Flask Web API は、api の URL 以外の URL にアクセスされると、public ディレクトリにあるファイルを返すようになっています。

Frontend のデバッグを開始するには、デバッグ設定「Launch Chrome」をデバッグ実行します。
実行すると、http://localhost:8080/ にアクセスするブラウザが立ち上がります。
表示されない場合には、下部ペインのポートタブを確認し、ポート転送されているポートを確認し、そのポートにアクセスしてください。

Web Frontend のコード [frontend/main.ts](frontend/main.ts) にブレークポイントを設定し、ブラウザ上で操作をして、main.ts がデバッグできていることを確認してください。

また、Web API にもブレークポイントを設定し、Web API とフロントエンドが組み合わされてデバッグできていることを確認してください。

## Docker コンテナを実行する

この DevContainer では、docker in docker がサポートされています。

以下のコマンドを実行すると、docker コンテナのビルドが行えます。

```
docker build .
```

## このリポジトリで実装されていること

- [(.devcontainer/devcontainer.json)](.devcontainer/devcontainer.json) で MySQL DB を含めた全ての全環境が立ち上がる
- initialize.py で、DB のテーブルの作成が行われる
