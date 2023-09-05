# Newspaper_OCR and Review
To run this repo, clone it using `git lfs clone https://github.com/dhruvchopra2003/Newspaper_ocr.git`.

If already cloned, pull the YOLO model using `git lfs pull`  

Upon cloning, create a new directory and name it `images` where you can input all the images.

Also, to ensure all the libraries are correctly installed, create a new virtual environment and run 
`pip install -r requirements.txt`

To start execution, `python monitor.py`
Refer to the official YOLO Documentation for further details about the image segmentation part of the project: [YOLOV8 Docs](https://docs.ultralytics.com/)
Additional Python Resources and libraries: [Watchdog](https://python-watchdog.readthedocs.io/en/stable/), [Pytesseract](https://pyimagesearch.com/2021/08/23/your-first-ocr-project-with-tesseract-and-python/), [TFIDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), NLTK etc. were used.
