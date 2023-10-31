import yaml
import webbrowser
import subprocess

with (open('setting.yml') as setting):
    setting = yaml.safe_load(setting)
    print(setting)
    # setting.yml open:web:url を読み込み、デフォルトのブラウザで表示する
    open_web_url = setting["open"]["web"]["url"]
    for web_url in open_web_url:
        try:
            webbrowser.open(web_url)
        except webbrowser.Error as err:
            print("exception web browser Error" + err)
        except Exception as err:
            print(err)
    # setting.yml open:app:pass を読み込み、appを起動する
    open_web_url = setting["open"]["app"]["pass"]
    for app_pass in open_web_url:
        try:
            subprocess.Popen(['open', app_pass])
        except subprocess.CalledProcessError as err:
            print("exception subprocess CalledProcessError" + err)
        except Exception as err:
            print(err)
