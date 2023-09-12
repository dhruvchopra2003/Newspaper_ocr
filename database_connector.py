import mysql.connector
from datetime import datetime


def connect_to_db():
    db = mysql.connector.connect(
        host="localhost", port=3308, user="root", password="", database="tesseract"
    )
    return db


def from_keyword_master(keyword_list, filename):
    db = connect_to_db()
    cursor = db.cursor()

    for key in keyword_list:
        query = f'SELECT keyId FROM keyword_master WHERE lower(keyWord) LIKE lower("{key}");'
        cursor.execute(query)
        keyid = cursor.fetchall()

        try:
            Insert_OcrKeywordlog(FileName=filename, KeyId=keyid[0][0])
        except:
            pass

    db.commit()
    cursor.close()
    db.close()


def Insert_OcrKeywordlog(
    FileName=None, KeyId=None, Keytype=None, clientid=None, priority=None
):
    db = connect_to_db()
    cursor = db.cursor()

    insert_sql = "INSERT INTO OcrKeywordlog (FileName, KeyId, keytype, clientid, priority) VALUES (%s, %s, %s, %s, %s);"
    insert_values = (FileName, KeyId, Keytype, clientid, priority)
    cursor.execute(insert_sql, insert_values)

    db.commit()
    cursor.close()
    db.close()


def Insert_OcrProcess(
    FileName=None,
    Status=None,
    Pubid=None,
    Pubdate=None,
    PageNo=None,
    Processed=None,
    Title=None,
    FolderPath=None,
    Full_Text=None,
    Date_folder=None,
    articleid=None,
    copied=None,
    Title2=None,
):
    db = connect_to_db()
    cursor = db.cursor()

    Date_Time = str(datetime.now())

    insert_sql = "INSERT INTO OcrProcess (FileName, Date_Time, Status, Pubid, Pubdate, PageNo, processed, Title, FolderPath, Full_Text, Date_Folder, articleid, copied, inserted, Title2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, NOW(), %s);"
    insert_values = (
        FileName,
        Date_Time,
        Status,
        Pubid,
        Pubdate,
        PageNo,
        Processed,
        Title,
        FolderPath,
        Full_Text,
        Date_folder,
        articleid,
        copied,
        Title2,
    )

    cursor.execute(insert_sql, insert_values)

    db.commit()
    cursor.close()
    db.close()


def delete_all_rows(table_name):
    db = connect_to_db()
    cursor = db.cursor()

    # Delete all rows from the ocr_tesseract table
    delete_sql_ocr = f"DELETE FROM {table_name}"

    # Delete all rows from the tesseract_keywords table
    # delete_sql_keywords = f"DELETE FROM tesseract_keywords"

    # cursor.execute(delete_sql_keywords)
    cursor.execute(delete_sql_ocr)

    db.commit()
    cursor.close()
    db.close()


def save_ocr_tesseract(name, path, article_list, headline_list):
    db = connect_to_db()
    cursor = db.cursor()
    insert_sql = "INSERT INTO ocr_tesseract (name, location) VALUES (%s, %s)"
    insert_values = (name, path)
    cursor.execute(insert_sql, insert_values)

    cursor.execute("SELECT LAST_INSERT_ID()")
    article_id = cursor.fetchone()[0]

    for word in headline_list:
        insert_keywords_sql = (
            "INSERT INTO tesseract_keywords (article_id, keywords) VALUES(%s, %s)"
        )
        insert_values = (article_id, word)
        cursor.execute(insert_keywords_sql, insert_values)

    for word in article_list:
        insert_keywords_sql = (
            "INSERT INTO tesseract_keywords (article_id, keywords) VALUES(%s, %s)"
        )
        insert_values = (article_id, word)
        cursor.execute(insert_keywords_sql, insert_values)

    db.commit()
    cursor.close()
    db.close()


# Call the function to delete all rows
# delete_all_rows("ocrprocess")
# delete_all_rows("ocrkeywordlog")
