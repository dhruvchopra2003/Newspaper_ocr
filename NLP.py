from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tag import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer

# # nltk.download('punkt')
# # nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')


def remove_bad_characters(s):
    bad_chars = [
        ";",
        ":",
        "|",
        "?",
        "*",
        "-",
        "$",
        ">",
        "<",
        "/",
        "%",
        "@",
        "~",
        "=",
        "{",
        "}",
        "(",
        ")",
        "[",
        "]",
        "_",
    ]

    s = "".join((filter(lambda i: i not in bad_chars, s)))
    return s


def get_keywords_2(article):
    words = word_tokenize(article)
    stop_words = set(stopwords.words("english"))
    fil = [word for word in words if word.lower() not in stop_words]

    pos_tags = pos_tag(fil)

    # Cutting off repeating words and prioritizing nouns
    unique_words = set()
    filtered_unique_words = []

    for word, pos in pos_tags:
        if word.lower() not in unique_words and pos.startswith("NN"):
            unique_words.add(word.lower())
            filtered_unique_words.append(word)

    word_freq = FreqDist(filtered_unique_words)
    keywords = [word for word in word_freq.most_common(20)]

    # k_str = ", ".join(keywords)
    return keywords


def get_keywords(lines):
    sentences = nltk.sent_tokenize(lines)

    keywords = []

    for sent in sentences:
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(sent))):
            if pos == "NN" or pos == "NNP" or pos == "NNS" or pos == "NNPS":
                keywords.append(word)

    return keywords


def get_keywords_blobs(txt):
    blob = TextBlob(txt)
    words = blob.noun_phrases

    stop_words = set(stopwords.words("english"))
    filtered = [
        word for word in words if word.lower() not in stop_words and len(word) > 2
    ]

    filtered = list(set(filtered))
    return filtered


def tf_extract(article):
    blob = TextBlob(article)
    sentences = blob.noun_phrases
    # sentences = blob.sentences
    corpus = [str(sentence) for sentence in sentences]

    vectorizer = TfidfVectorizer(max_features=30)  # Adjust max_features as needed
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Get feature names (keywords) with highest TF-IDF scores
    keywords = vectorizer.get_feature_names_out()
    stops = set(stopwords.words("english"))
    keywords = list(set(keywords))

    keywords = [key for key in keywords if key.lower() not in stops and len(key) > 3]

    return keywords


from transformers import BertTokenizer, BertForMaskedLM
import torch


def extract_keywords_bert(article):
    # Load pre-trained BERT model and tokenizer
    model_name = "bert-base-uncased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForMaskedLM.from_pretrained(model_name)

    # Split the article into smaller segments
    segment_length = 512  # Maximum token limit for BERT
    segments = [
        article[i : i + segment_length] for i in range(0, len(article), segment_length)
    ]

    # Initialize the list of keywords
    keywords = []

    # Process each segment
    for segment in segments:
        # Tokenize the segment
        tokens = tokenizer.encode(segment, add_special_tokens=True, return_tensors="pt")

        # Get model predictions
        with torch.no_grad():
            outputs = model(tokens)
            predictions = outputs.logits

        # Find the tokens with highest probabilities
        top_token_indices = predictions.argmax(dim=2)

        # Convert token indices to words
        segment_keywords = [tokenizer.decode(idx) for idx in top_token_indices[0]]

        # Filter out special tokens and add to the list of keywords
        segment_keywords = [
            kw for kw in segment_keywords if kw not in tokenizer.all_special_tokens
        ]
        keywords.extend(segment_keywords)

    # Remove duplicates
    filtered_keywords = list(set(keywords))
    return filtered_keywords
