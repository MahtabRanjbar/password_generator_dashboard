# password_generator.py

import random
import string
import re
from abc import ABC, abstractmethod
from typing import List, Optional
import nltk


nltk.download('words', quiet=True)


class PasswordGenerator(ABC):
    """
    Abstract base class for generating passwords.
    """
    @abstractmethod
    def generate(self) -> str:
        """
        Generate a password.

        Returns:
            str: The generated password.
        """
        pass


class RandomPasswordGenerator(PasswordGenerator):
    """
    Class to generate a random password.
    """
    def __init__(self, length: int = 8, include_numbers: bool = False, include_symbols: bool = False):
        """
        Initialize the RandomPasswordGenerator.

        Args:
            length (int): Length of the password.
            include_numbers (bool): Whether to include numbers in the password.
            include_symbols (bool): Whether to include symbols in the password.
        """
        self.length = length
        self.characters = string.ascii_letters
        if include_numbers:
            self.characters += string.digits
        if include_symbols:
            self.characters += string.punctuation

    def generate(self) -> str:
        """
        Generate a random password from specified characters.

        Returns:
            str: The generated random password.
        """
        return ''.join(random.choice(self.characters) for _ in range(self.length))


class MemorablePasswordGenerator(PasswordGenerator):
    """
    Class to generate a memorable password.
    """
    def __init__(
        self,
        no_of_words: int = 5,
        separator: str = "-",
        capitalization: bool = False,
        vocabulary: Optional[List[str]] = None
    ):
        """
        Initialize the MemorablePasswordGenerator.

        Args:
            no_of_words (int): Number of words in the password.
            separator (str): Separator between words.
            capitalization (bool): Whether to capitalize words.
            vocabulary (Optional[List[str]]): List of words to choose from.
        """
        if vocabulary is None:
            vocabulary = nltk.corpus.words.words()
        self.no_of_words = no_of_words
        self.separator = separator
        self.capitalization = capitalization
        self.vocabulary = [word for word in vocabulary if len(word) >= 3 and word.isalpha()]

    def generate(self) -> str:
        """
        Generate a memorable password from a list of vocabulary words.

        Returns:
            str: The generated memorable password.
        """
        password_words = [random.choice(self.vocabulary) for _ in range(self.no_of_words)]
        if self.capitalization:
            password_words = [word.capitalize() for word in password_words]
        return self.separator.join(password_words)


class PinCodeGenerator(PasswordGenerator):
    """
    Class to generate a numeric pin code.
    """
    def __init__(self, length: int = 4):
        """
        Initialize the PinCodeGenerator.

        Args:
            length (int): Length of the pin code.
        """
        self.length = length

    def generate(self) -> str:
        """
        Generate a numeric pin code.

        Returns:
            str: The generated pin code.
        """
        return ''.join(random.choice(string.digits) for _ in range(self.length))


def check_password_strength(password: str) -> str:
    """
    Check the strength of a given password.

    Args:
        password (str): The password to check.

    Returns:
        str: The password strength ('Weak', 'Medium', or 'Strong').
    """
    if len(password) < 8:
        return 'Weak'
    elif len(password) < 12:
        if re.match(r'^[a-zA-Z]+$', password):
            return 'Weak'
        elif re.match(r'^[a-zA-Z0-9]+$', password):
            return 'Medium'
    return 'Strong'

