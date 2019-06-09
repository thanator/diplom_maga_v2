import re

import pymorphy2


def format_text(text: str, fullFormat: bool = 'true') -> str:
    rexText1 = re.sub('<\s*ref[^>]*\/\s*>', "", text)
    if fullFormat:
        rexText1 = re.sub('<\s*ref[^>]*\s*>([^~]*)<\s*\/\s*ref\s*>', "", rexText1)
    return re.sub('[^а-яА-Я0-9 ]', "", rexText1)


def get_normal_form_of_word(word: str) -> str:
    return pymorphy2.MorphAnalyzer().parse(word)[0].normal_form
