from impact_ocr import execute
import os

if __name__ == "__main__":
    for i in os.listdir("images"):
        temp = os.path.join("images", i)
        execute(temp)
