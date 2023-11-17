import re
import os
import glob
import psycopg2 as db_adapter
from psycopg2.extras import DictCursor
from google.cloud import vision
from dotenv import load_dotenv


# OCR対象のファイルを取得
# 取得したファイルをVisionAPIに連携し、OCRデータを返却する
def get_ocr(ocr_file_path):
    client = vision.ImageAnnotatorClient()
    with open(ocr_file_path, "rb") as ocr_file:
        content = ocr_file.read()
    image = vision.Image(content=content)
    response_ocr = client.text_detection(image=image)
    return response_ocr


# OCRから材料に関する情報を取得
# 材料を辞書型（name：OCR, price：OCR）のペアでリスト追加し返却する
def get_material_dic_list(ocr_date):
    ocr_full_text = ocr_date.full_text_annotation.text
    ocr_sep_list = ocr_full_text.splitlines()
    material_list = []
    for ocr_text in ocr_sep_list:
        ocr_text = ocr_text.replace(" ", "")
        if not ocr_text.startswith("¥") and "¥" in ocr_text:
            new_ocr_text = ocr_text.split("¥")
            material_list.append(new_ocr_text[0])  # 材料
            material_list.append(new_ocr_text[1])  # 金額
        else:
            new_ocr_text = re.sub('¥', '', ocr_text)
            material_list.append(new_ocr_text)
    material_dicts = []
    for i in range(len(material_list)):
        if i % 2 != 0:
            material_dictionary = {"name": material_list[i - 1], "price": material_list[i]}
            material_dicts.append(material_dictionary)
    return material_dicts


# db接続する
def db_adapter_connect():
    load_dotenv()
    env_dbname = os.environ["DB_NAME"]
    env_host = os.environ["DB_HOST"]
    env_user = os.environ["DB_USER"]
    env_password = os.environ["DB_PASSWORD"]
    connect = db_adapter.connect(database=env_dbname,
                                 host=env_host,
                                 user=env_user,
                                 password=env_password)

    return connect


def get_update_info_dic(is_update, update_id, update_price, ocr_name, message):
    update_info = {"is_update": is_update,
                   "update_id": update_id,
                   "update_price": update_price,
                   "ocr_name": ocr_name,
                   "message": message}

    return update_info


# 材料に関するOCRを元に、アップデート処理に関する情報を取得
# アップデート処理を行うもの、そうでないものの情報を辞書型のペアでリスト追加し返却する
# 　is_update：True or False,
# 　update_id：レコードを示す一意な値,
# 　update_price:OCRの材料名,
# 　ocr_name:OCRの金額,
# 　message:情報に関するメッセージ
def get_update_info(material_dicts):
    conn = db_adapter_connect()
    cur = conn.cursor(cursor_factory=DictCursor)
    update_info_dic_list = []
    for material_dic in material_dicts:
        query = "select id from material_mst where search_text like '%" + material_dic.get("name") + "%';"
        cur.execute(query)
        query_record = cur.fetchall()

        if query_record:
            if len(query_record) == 1:
                update_info_dic = get_update_info_dic(True,
                                                      query_record[0].get("id"),
                                                      material_dic.get("price"),
                                                      material_dic.get("name"),
                                                      "更新しました"
                                                      )
            else:
                update_info_dic = get_update_info_dic(False,
                                                      "-",
                                                      "-",
                                                      material_dic.get("name"),
                                                      "複数のレコードと紐づいたため、更新対象から外しました"
                                                      )
        else:
            update_info_dic = get_update_info_dic(False,
                                                  "-",
                                                  "-",
                                                  material_dic.get("name"),
                                                  "紐づくレコードがありませんでした"
                                                  )
        update_info_dic_list.append(update_info_dic)
    cur.close()
    conn.close()
    return update_info_dic_list


def update_db(update_id, price):
    conn = db_adapter_connect()
    cur = conn.cursor()
    query = "UPDATE material_mst SET price = %s WHERE id = %s"
    cur.execute(query, (price, update_id))
    conn.commit()
    cur.close()
    conn.close()


# 更新対象の情報は更新処理を行う
# 更新対象でない情報も含め、処理結果をログ出力する
def update_or_log(update_info):
    for index, info in enumerate(update_info):
        index += 1
        if info.get("is_update"):
            update_db(info.get("update_id"), info.get("update_price"))
        name = info.get("ocr_name")
        message = info.get("message")
        log = f"{index}：{name}|{message}"
        print(log)


receipt_paths = glob.glob('receipt/*.jpg')
for receipt_path in receipt_paths:
    ocr = get_ocr(receipt_path)
    material_dic_list = get_material_dic_list(ocr)
updated_or_not = get_update_info(material_dic_list)
update_or_log(updated_or_not)
