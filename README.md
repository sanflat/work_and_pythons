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
