import mysql.connector


def connect_to_db():
    db = mysql.connector.connect(
        host="localhost", port=3306, user="root", password="1234", database="tesseract"
    )
    return db


def create_OcrKeywordlog(db):
    cursor = db.cursor()

    create_table_query = """CREATE TABLE OcrKeywordlog (
    ID INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    FileName VARCHAR(50) NOT NULL UNIQUE,
    KeyId INT(10) UNSIGNED NOT NULL,
    keytype VARCHAR(250),
    clientid VARCHAR(45),
    priority VARCHAR(45)
    )"""

    cursor.execute(create_table_query)
    cursor.close()
    db.commit()
    db.close()

    print("table created")

def create_OcrProcess(db):
    cursor = db.cursor()

    create_table_query = """CREATE TABLE OcrProcess (
        ID INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        FileName VARCHAR(50) UNIQUE,
        Date_Time VARCHAR(45),
        Status INT(10) UNSIGNED default 0,
        Pubid int(10) unsigned,
        PubDate VARCHAR(45),
        PageNo VARCHAR(45),
        Processed VARCHAR(10) default 0,
        Title VARCHAR(1000),
        FolderPath VARCHAR(50),
        Full_Text longtext,
        Date_Folder varchar(50),
        articleid varchar(50),
        copied int(5) default 0,
        inserted datetime,
        Title2 text
    )"""

    cursor.execute(create_table_query)
    cursor.close()
    db.commit()
    db.close()

    print("Created table")

create_OcrKeywordlog(connect_to_db())
# create_OcrProcess(connect_to_db())



