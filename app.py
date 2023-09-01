from impact_ocr import execute
import argparse
import os
# parser = argparse.ArgumentParser()
# parser.add_argument("--file_path", type=str, help="Path of the file added")
# args = parser.parse_args()
# print("check 3")

if __name__ == "__main__":
    for i in os.listdir("images"):
        temp = os.path.join("images", i)
        execute(temp)


    # print("Added file path is: ", args.file_path)
    # print("Added file path type is: ", type(args.file_path))
    # execute(args.file_path)

# Enter image path: images\test9.jpg
# Added file path is:  'images\test9.jpg'