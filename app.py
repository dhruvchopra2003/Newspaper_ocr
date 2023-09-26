from impact_ocr import execute
import os
import glob

if __name__ == "__main__":
    print("Request recieved from monitor.py")

    directory_name = r'\\192.168.248.31\irisprocess\tesseract\input'
    # directory_name = "images"

    # output_dir = rf'\\192.168.248.31\irisprocess\tesseract\output'
    # output_dir = f"outputs_without_keywords"



    jpg_files = glob.glob(os.path.join(directory_name,"*.jpg"))    
    if len(jpg_files) != 0:
        for i in os.listdir(directory_name):
            if i.endswith(".jpg"):
                temp = os.path.join(directory_name, i)
                execute(temp)
            else:
                print("Not an image, requesting removal...")
                continue

    print("Beginning Monitoring...")
    os.system("python monitor.py")


    # for i in os.listdir("images"):
    #     temp = os.path.join("images", i)
    #     execute(temp)
