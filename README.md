# Newspaper_OCR and Review
To run this repo, clone it using `git lfs clone https://github.com/dhruvchopra2003/Newspaper_ocr.git`.

If already cloned, pull the YOLO model using `git lfs pull`  

Upon cloning, create a new folder and name it `images` where you can input all the images.

Also, to ensure all the libraries are correctly installed, create a new virtual environment and run 
`pip install -r requirements.txt`

To start execution, run `python monitor.py`

## Sources and References:
- Image segmentation and headline extraction: [YOLOV8 Docs](https://docs.ultralytics.com/)
- Text Interpretation: [Pytesseract](https://pyimagesearch.com/2021/08/23/your-first-ocr-project-with-tesseract-and-python/)

### Additional Python Resources and libraries:
- [Watchdog](https://python-watchdog.readthedocs.io/en/stable/),
- For NLP related tasks:
  - [TFIDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
  - [NLTK](https://www.nltk.org/) etc.

- Refer to the [jupyter notebook](https://github.com/dhruvchopra2003/Newspaper_ocr/blob/master/pytesseract.ipynb) for the image acquisition and preprocessing techniques, model training, and other different pipelines related to the project.
