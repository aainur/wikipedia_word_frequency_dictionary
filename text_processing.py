import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_and_tokenize(text: str):
    """
    Clean the text by removing unwanted characters, normalizing, and tokenizing the text.
    Args:
        text (str): The input article text.
    Returns:
        list: A list of processed words.
    """
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = text.split()
    cleaned_words = [
        lemmatizer.lemmatize(word) for word in words if word not in stop_words
    ]
    return cleaned_words

def get_word_frequency(text: str):
    words = clean_and_tokenize(text)
    word_counts = Counter(words)
    return word_counts