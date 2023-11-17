# キャッチフレーズ
「普段の単調な作業のお供にPython」  

# リポジトリについて
Python学習のアウトプットプログラムを格納するリポジトリ。  
普段の単調な作業をPythonプログラムで解決する。

# 各種プログラムの説明
## work_and_pythons/open_hassle  
**機能の概要**  
毎回表示しているWEBサイトやOSのアプリケーションを自動で開く  

**使う手順**  
1. setting.ymlにWEBサイトのURLやOSのアプリケーションパスを指定する
2. open.pyを実行する
3. setting.ymlで指定したWEBサイトやアプリケーションが表示される

**使用したモジュール**  
+ ymlファイルの読み込み：https://pyyaml.org
+ WEBサイトを開く処理：https://docs.python.org/ja/3/library/webbrowser.html
+ アプリを開く処理：https://docs.python.org/ja/3/library/subprocess.html

**その他情報**  
・ソースコードの説明や使用方法に関する記事（qiita）  
https://qiita.com/pooh-hey/items/1c20f740c3f028a631e9  
  
・MAC起動時にWebサイトとappを自動で開く方法(note)  
https://note.com/hey07/n/nc9b03378da09  

## work_and_pythons/notify_of_query_results  
**機能の概要**  
クエリ結果をメッセージとして通知する  
通知する方法として、SlackやGmailなどを想定している
方法別にPythonプログラムを作成する

**使う手順**  
1. envファイルにDB接続情報（PostgreSQL）を記載する
2. 通知する方法に応じてenvファイルに接続情報を記載する（例えばSlackであれば、Slack APIトークンや）
3. 通知する方法に応じてPythonプログラムを実行する

**事前準備（Slackで通知する場合）**  
Slack APIから、アプリの作成とAPI_TOKENの取得を行う必要がある
1. slack api(https://api.slack.com/) からアプリを作成
2. Permissions -> Scopeからchat:write権限を追加
3. slackワークスペースにアプリをインストール
4. 通知するチャンネルにアプリを追加する
5. Bot User OAuth Access TokenのAPI tokenを取得する

**使用したモジュール**  
+ ワイルドカードを含むパスでファイルを取得する：https://docs.python.org/ja/3/library/glob.html
+ PostgreSQLへの接続：https://pypi.org/project/psycopg2/
+ 環境ファイルの設定値を取得する：https://docs.python.org/ja/3/library/os.html
+ 環境ファイルの設定値を読み込む：https://pypi.org/project/python-dotenv/
+ 環境ファイルの設定値を読み込む：https://pypi.org/project/python-dotenv/
+ Slackアプリとのやりとり：https://slack.dev/python-slack-sdk/

**その他情報**  
・クエリの結果を、Slackアプリに通知する  
https://qiita.com/pooh-hey/items/e2c77a06a31f4f40a9ed  

## work_and_pythons/ocr_to_db
**機能の概要**  
レシートデータを元にDBのデータを更新する  
VisionAPIを使用し、OCRを取得  
OCRから、料理に使う材料と金額を取得しDB更新を行う
