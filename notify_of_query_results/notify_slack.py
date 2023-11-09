import glob
import psycopg2 as db_adapter
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def get_query_result():
    # 発行するクエリを記載したsqlファイルのパスをリスト取得
    sql_file_paths = glob.glob('sql/*.sql')
    # sqlファイル数分のループ処理を行い、クエリ結果を取得する
    for sql_file_path in sql_file_paths:
        file = open(sql_file_path)
        query = file.read()
        # .envから、DB接続に用いる情報を取得
        load_dotenv()
        env_dbname = os.environ["DB_NAME"]
        env_host = os.environ["DB_HOST"]
        env_user = os.environ["DB_USER"]
        env_password = os.environ["DB_PASSWORD"]
        conn = db_adapter.connect(dbname=env_dbname, host=env_host, user=env_user, password=env_password)
        # sql結果をリスト取得するため引数にDictCursorを指定
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute(query)
        query_column = [col.name for col in cur.description]
        query_record = cur.fetchall()
        cur.close()
        conn.close()
        result = [{"column": query_column}, {"record": query_record}]
        return result


def notify_slack(channel):
    results = get_query_result()
    text_column = ', '.join(results[0]["column"])
    text_record = ''
    for r in results[1]["record"]:
        text_record += r[0] + ',' + r[1] + "\r\n"
    # text_resultは以下のような形になる
    # カラム名
    # レコード1
    # レコード2...
    text_result = text_column + "\r\n" + text_record
    slack_token = os.environ["SLACK_API_TOKEN"]
    client = WebClient(token=slack_token)
    try:
        client.chat_postMessage(channel=channel, text=text_result)
    except SlackApiError as e:
        assert e.response["error"]


# アプリを追加し、メッセージを投稿したいチャンネル名を指定
load_dotenv()
notify_slack(os.environ["SLACK_CHANNEL"])
