# Translator for the GemEssayGenerator
# Author Sami Chemali
from deep_translator import GoogleTranslator


def translate(string, lang, langofessay):
    translation = ""
    if lang == "en" and langofessay == "en":
        translation = string[0:5000]
    else:
        string = string[0:6000]
        while translation == "":
            try:
                translation = GoogleTranslator(source='auto', target=lang).translate(string)
            except:
                string = string[0: (len(string) - 100)]
    return translation
