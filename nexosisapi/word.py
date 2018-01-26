from enum import Enum


class WordType(Enum):
    word = 0,
    stop_word = 1

class Word(object):
    """A word from a vocabulary"""

    def __init__(self, data_dict=None):
        if data_dict is None:
            data_dict = {}

        self._text = data_dict.get('text', '')
        self._type = None
        word_type = data_dict.get('type', None)
        if word_type:
            self._type = WordType(word_type)

        self._rank = data_dict.get('rank', None)


    @property
    def text(self):
        """The text of the word"""
        return self._text

    @property
    def type(self):
        """The type of the word (Word or Stop Word)"""
        return self._type

    @property
    def rank(self):
        """The importance rank of the word"""
        return self._rank


