from impact_ocr import execute
import os

if __name__ == "__main__":
    print("Request recieved from monitor.py")
    # for i in os.listdir(r'\\192.168.248.31\irisprocess\tesseract\input'):
    #     temp = os.path.join(r'\\192.168.248.31\irisprocess\tesseract\input', i)
    #     execute(temp)
    for i in os.listdir("images"):
        temp = os.path.join("images", i)
        execute(temp)
