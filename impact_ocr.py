import pytesseract as ps
import shutil
import os
import random
import cv2
from PIL import Image
import numpy as np
from PIL import Image, ImageDraw
import textwrap
import NLP

# from roboflow import Roboflow
from ultralytics import YOLO
from os import listdir


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
        text_with_separator = article.replace("\n\n", paragraph_separator)

        # Wrap text at a maximum width of 80 characters
        wrapped_text = textwrap.fill(text_with_separator, width=80)

        # Restore paragraph separations by replacing the unique separator
        article = wrapped_text.replace(paragraph_separator, "\n\n")
        article = article.replace("- ", "")

        # article = textwrap.fill(article, width=80)
        return article

    @staticmethod
    def tesseract_read(img_path):
        info = ps.image_to_string(Image.open(img_path))
        return info


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
            os.mkdir(directory_path)
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


# def execute():
def execute(img_path):
    # img_path = input("Enter image path: ")
    
    # model_path = "models\\best.pt"
    model_path = os.path.join(".", "models", "best.pt")

    image_name = FileHandler.get_name(img_path)

    ocr_processor = OCRProcessor(model_path)
    ocr_processor.yolo_ocr(img_path)

    keywords = []

    headline = TextExtractor.read_header(f"runs/detect/predict/crops/headlines/")
    
    keywords = NLP.get_keywords_blobs(headline)
    # keywords = NLP.get_keywords(headline)
    # keywords = NLP.extract_keywords_bert(headline)
    # keywords = NLP.tf_extract(headline)
    # keywords = NLP.get_keywords_2(headline)
    
    article_body = TextExtractor.read_article(img_path)
    
    art_k = NLP.get_keywords_blobs(article_body)
    # art_k = NLP.get_keywords(article_body)
    # art_k = NLP.extract_keywords_bert(article_body)
    # art_k = NLP.tf_extract(article_body)
    # art_k = NLP.get_keywords_2(article_body)
    
    keys = ""
    for k in keywords:
        keys = keys + "\n" + str(k) 

    for k in art_k:
        keys = keys + '\n' + str(k)

    FileHandler.delete_runs_dir()

    output_directory = (
        # f"/content/gdrive/MyDrive/Impact_OCR/output/test_images/{image_name[:-3]}"
        f"results/{image_name[:-3]}"
    )
    FileHandler.create_directory(output_directory)

    FileHandler.save_content(output_directory, "headline.txt", headline)
    FileHandler.save_content(output_directory, "article.txt", article_body)
    FileHandler.save_content(output_directory, "keywords.txt", keys)
    FileHandler.save_img(img_path ,output_directory, image_name)
    print("Execution completed.")


if __name__ == "__main__":
    execute()