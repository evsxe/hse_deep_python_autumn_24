from io import StringIO
from typing import Union, List


def reading_filtering_generator(
        filename: Union[str, StringIO],
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
        with open(filename, 'r', encoding='UTF8') as file_object:
            for row in file_object:
                yield from row_filter(row)

    elif isinstance(filename, StringIO):
        for row in filename:
            yield from row_filter(row)
