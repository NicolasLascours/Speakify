import re
from nltk.tokenize import sent_tokenize
from langdetect import detect
from deep_translator import GoogleTranslator


def clean_txt_text(raw_text):
    try:
        cleaned_text = raw_text.replace('\t', ' ')
        return cleaned_text
    except Exception as clean_txt_error:
        print(f"Error cleaning TXT text: {clean_txt_error}")
        raise clean_txt_error

def read_txt(txt_file):
    try:
        with open(txt_file, "r", encoding="utf-8") as file:
            raw_text = file.read()
            cleaned_text = clean_txt_text(raw_text)
        return cleaned_text
    except Exception as txt_error:
        print(f"Error reading TXT: {txt_error}")
        raise txt_error

def detect_language(text):
    """
    Detecta el idioma del texto.
    """
    try:
        return detect(text)
    except Exception as language_detection_error:
        print(f"Error detecting language: {language_detection_error}")
        raise language_detection_error

def split_text_into_sentences(text):
    """
    Divide el texto en oraciones.
    """
    try:
        return sent_tokenize(text)
    except Exception as sentence_split_error:
        print(f"Error splitting text into sentences: {sentence_split_error}")
        raise sentence_split_error


def translate_sentence(sentence, target_lang='es'):
    """
    Traduce una oración al idioma especificado.
    """
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(sentence)
    except Exception as translate_sentence_error:
        print(f"Error translating sentence: {translate_sentence_error}")
        raise translate_sentence_error