from typing import Union, List, IO

"""
Task Description:
    Есть текстовый файл, который может не помещаться в память.
    В каждой строке файла фраза или предложение: набор слов,
     разделенных пробелами (знаков препинания нет).

    Генератор должен принимать на вход:

    - имя файла или файловый объект;
    - список слов для поиска;
    - список стоп-слов.

    Генератор перебирает строки файла и возвращает только те из них
     (строку целиком), где встретилось хотя бы одно из слов для поиска.
    Если в одной строке сразу несколько совпадений, то вернуть строку
    надо лишь один раз. Если в строке встретилось слово из списка стоп-слов,
    то такая строка должна игнорироваться, даже если там есть совпадения по
    словам поиска. Поиск совпадений и стоп-слов должен выполняться по полному
     совпадению слова без учета регистра.

    Например, для строки из файла "а Роза упала на лапу Азора" слово поиска
    "роза" должно найтись, а "роз" или "розан" - уже нет. В случае той же строки
    "а Роза упала на лапу Азора", слова-совпадения "роза" и стоп-слова "азора"
     исходная строка должна будет быть отброшена.
"""


def reading_filtering_generator(
        filename: Union[str, IO],
        search_words: List[str],
        stop_words: List[str]
) -> str:
    """
    :param filename: file name or file object.
    :param search_words: a list of words to search for.
    :param stop_words: stop word list.
    :yields: lines from the file containing at least one word
                from the search list and no stop words.
    """

    search_words = set(search_words)
    stop_words = set(stop_words)

    def row_filter(row: str) -> str:
        words = row.lower().split()
        exist_search_words = any(word in words for word in search_words)
        exist_stop_words = any(word in words for word in stop_words)
        if exist_search_words and not exist_stop_words:
            yield row

    if isinstance(filename, str):
        with open(filename, 'r') as file_object:
            for row in file_object:
                yield from row_filter(row)

    elif isinstance(filename, IO):
        for row in filename:
            yield from row_filter(row)
