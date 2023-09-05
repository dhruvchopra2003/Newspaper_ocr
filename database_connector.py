import mysql.connector


def connect_to_db():
    db = mysql.connector.connect(
        host="localhost", port=3308, user="root", password="", database="tesseract"
    )
    return db


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


# cursor.close()
# db.close()

# import mysql.connector

def delete_all_rows():
    db = connect_to_db()
    cursor = db.cursor()

    # Delete all rows from the ocr_tesseract table
    delete_sql_ocr = "DELETE FROM ocr_tesseract"

    # Delete all rows from the tesseract_keywords table
    delete_sql_keywords = "DELETE FROM tesseract_keywords"
    
    cursor.execute(delete_sql_keywords)
    cursor.execute(delete_sql_ocr)

    db.commit()
    cursor.close()
    db.close()

# Call the function to delete all rows
# delete_all_rows()
