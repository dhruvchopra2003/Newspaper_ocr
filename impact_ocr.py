import pytesseract as ps
import shutil
import os
from PIL import Image
from PIL import Image
import textwrap
import NLP
import database_connector as dbc
from datetime import date
import datetime
from ultralytics import YOLO
from os import listdir
import create_template


# Class for initializing the YOLO Image segmentation OCR process
class OCRProcessor:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def yolo_ocr(self, img_path):
        results = self.model.predict(
            source=img_path,
            save_txt=True,
            save=True,
            save_crop=True,
            hide_labels=True,
            # line_thickness=1
        )
        return results

    def tesseract_read(self, img_path):
        info = ps.image_to_string(Image.open(img_path))
        return info


# Class to read text, using Pytesseract
class TextExtractor:
    @staticmethod
    def combine_sentences(sentence1, sentence2):
        words1 = sentence1.split()
        words2 = sentence2.split()

        # Find the common suffix length
        common_suffix_length = 0
        for i in range(1, min(len(words1), len(words2)) + 1):
            if words1[-i] == words2[-i]:
                common_suffix_length = i
            else:
                break

        # Combine sentences with newline if no common suffix
        if common_suffix_length == 0:
            combined_sentence = sentence1 + "\n" + sentence2
        else:
            combined_sentence = " ".join(words1 + words2[:-common_suffix_length])

        return combined_sentence

    @staticmethod
    def read_header(header_path):
        folder_dir = header_path
        header = ""

        for images in os.listdir(folder_dir):
            if images.endswith(".jpg"):
                temp_path = header_path + images
                temp = TextExtractor.tesseract_read(temp_path)
                temp = temp.replace("\n", " ")
                # header += temp
                header = TextExtractor.combine_sentences(header, temp)

            # header += '\n'
            # header = header.replace('\n', ' ')
        return header

    @staticmethod
    def read_article(img_path):
        article = TextExtractor.tesseract_read(img_path)

        paragraph_separator = "___PARAGRAPH_SEPARATOR___"
        # text_with_separator = article.replace("\n\n", "</p>" + paragraph_separator + "<p>")
        text_with_separator = article.replace("\n\n", paragraph_separator)

        # Wrap text at a maximum width of 100 characters
        wrapped_text = textwrap.fill(text_with_separator, width=100)

        # Restore paragraph separations by replacing the unique separator
        article = wrapped_text.replace(paragraph_separator, "\n\n")
        article = article.replace("- ", "")

        # article = textwrap.fill(article, width=80)
        return article

    @staticmethod
    def tesseract_read(img_path):
        info = ps.image_to_string(Image.open(img_path))
        return info


# Class to extract the article details given in the image name
class ArticleDetails:
    @staticmethod
    def get_info(image_name):
        temp_list = image_name.split("-")
        pubid = temp_list[0]
        pubdate = temp_list[1]
        page_no = temp_list[2]
        page_name = temp_list[3]

        return pubid, pubdate, page_no, page_name


# Consists of various useful file handling functions
class FileHandler:
    @staticmethod
    def get_name(path):
        image_name = os.path.basename(path)
        return image_name

    @staticmethod
    def save_content(folder_path, file_name, content):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Content saved to {file_path}")

    @staticmethod
    def save_img(source, destination, img_name):
        destination = os.path.join(destination, img_name)
        shutil.move(source, destination)
        print("Image moved")

    @staticmethod
    def create_directory(directory_path):
        try:
            # os.mkdir(directory_path, exist_ok=True)
            os.makedirs(directory_path, exist_ok=True)
        except FileExistsError:
            print("Directory already exists")

    @staticmethod
    def delete_directory(directory_path):
        try:
            shutil.rmtree(directory_path)
        except Exception as e:
            print(f"Error occurred while deleting directory: {e}")

    @staticmethod
    def delete_runs_dir():
        path = "runs"
        try:
            shutil.rmtree(path)
            print("deleted runs")
        except:
            print("Error occured while deleting runs")


# Main function for execution, Called from app.py
def execute(img_path):
    model_path = os.path.join(".", "models", "best2.pt")

    # Extracting necessary credentials
    image_name = FileHandler.get_name(img_path)
    pubid, pubdate, page_no, page_name = ArticleDetails.get_info(image_name)
    # currentDate = date.today()
    currentDatetime = datetime.datetime.now()
    currentDate = currentDatetime.strftime("%Y%m%d")

    # Defining the output directories
    output_directory = (
        f"outputs_without_keywords\{str(currentDate)}"
        # rf"\\192.168.248.31\irisprocess\tesseract\output\{str(currentDate)}"
    )

    FileHandler.create_directory(output_directory)
    html_folder = os.path.join(output_directory, "html")
    images_folder = os.path.join(output_directory, "images")
    text_folder = os.path.join(output_directory, "text")
    headlines_folder = os.path.join(output_directory, "headlines")

    # Creating the directories for saving the outputs
    FileHandler.create_directory(html_folder)
    FileHandler.create_directory(images_folder)
    FileHandler.create_directory(text_folder)
    FileHandler.create_directory(headlines_folder)

    html_path = os.path.join(html_folder, f"{image_name}.html")

    # Initializing the OCR process class and to get image segmentation
    ocr_processor = OCRProcessor(model_path)
    ocr_processor.yolo_ocr(img_path)

    # Reading the headline text using pytessseract
    headline = "-"
    try:
        headline = TextExtractor.read_header(f"runs/detect/predict/crops/headlines/")
    except:
        print("No headline")

    # Reading the article text using pytesseract
    article_body = TextExtractor.read_article(img_path)

    # List of functions and pipelines available for extracting important words, full text to list
    # art_k = NLP.remove_stop_words(article_body)
    art_k = NLP.get_keywords_blobs(article_body)
    # art_k = NLP.get_keywords(article_body)
    # art_k = NLP.extract_keywords_bert(article_body)
    # art_k = NLP.tf_extract(article_body)
    # art_k = NLP.get_keywords_2(article_body)

    # Cleaning the list
    keys = []
    for k in art_k:
        k = NLP.remove_bad_characters(k)
        x = k.split()
        for i in x:
            keys.append(str(i))
        # keys = keys + '\n' + str(k)

    # Saving the data in OcrProcess Table
    # try:
    #     print("Inserting data into OcrProcess...")
    #     dbc.Insert_OcrProcess(
    #         FileName=image_name,
    #         Pubid=pubid,
    #         Pubdate=pubdate,
    #         PageNo=page_no,
    #         Title=headline,
    #         FolderPath=str(output_directory),
    #         Full_Text=article_body,
    #         Date_folder=currentDate,
    #     )

    # except:
    #     print("FileName already exists in the table")

    # # Inserting data into ocrkeywordlog table, by matching keywords from keyword_master
    # try:
    #     print("Entering KeyIds into ocrkeywordlog...")
    #     dbc.from_keyword_master(keys, image_name)
    # except Exception as exp:
    #     print(exp)

    # Saving the contents into Text and HTML files
    try:
        FileHandler.save_content(headlines_folder, f"{image_name}.txt", headline)
    except:
        print("No Header Saved")

    # Creating HTML template
    try:
        temp_img_path = os.path.join("runs/detect/predict/crops/image/", image_name)
        FileHandler.save_img(
            source=temp_img_path, destination=html_folder, img_name=image_name
        )
        img_dest_path = os.path.join(html_folder, image_name)
        create_template.create_html_with_img(
            headline, article_body, html_path, img_dest_path
        )
    except:
        create_template.create_html(headline, article_body, html_path)

    # Deleting the temporary runs folder made by the YOLO library
    FileHandler.delete_runs_dir()

    FileHandler.save_content(text_folder, f"{image_name}.txt", article_body)
    FileHandler.save_img(img_path, images_folder, image_name)

    # FileHandler.save_content(html_folder, f"{image_name}.html", article_body)
    # FileHandler.save_content(output_directory, "keywords.txt", keys)

    print("Execution completed.")
