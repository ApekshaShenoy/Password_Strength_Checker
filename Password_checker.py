import tkinter as tk                                                                                         # GUI library for creating the application interface
from tkinter import filedialog, messagebox
import re                                                                                                    # Regular expression module for password validation 
import random                                                                                                # Module for generating random passwords
import string                                                                                                # Module for string operations, used in password generation
import logging                                                                                               # Module for logging password check results
import json                                                                                                  # Module for handling JSON data, used for saving password check results
import argparse                                                                                              # Module for parsing command-line arguments
import sys                                                                                                   # Module for system-specific parameters and functions, used for exiting the application
import funtools                                                                                              # Module for caching results of expensive function calls, used for optimizing password strength checks
from functools import lru_cache
from zxcvbn import zxcvbn                                                                                   # Library for password strength estimation

# Configure logging to write password check results to a file   
logging.basicConfig(filename='password_checker.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Wordlist:

    # Class variable to cache loaded wordlists
    _cache = {} 

    def __init__(self,file_path):
        self.file_path = file_path
        self.words = self.load_wordlist()

    def load_wordlist(self):
        # Check if the wordlist is already cached
        if self.file_path in self._cache:
            return self._cache[self.file_path]
        
        try:
            with open(self.file_path, 'r',encoding='utf-8') as file:
                Wordlist = [line.strip() for line in file ]
                self._cache[self.file_path] = Wordlist
                return Wordlist
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error: File '{self.file_path}' not found.") from e
        except Exception as e:
            raise RuntimeError(
                f"Error loading worklist from {self.file_path}: {str(e)}"
            )from e
        
        
        def is_word_in_list(self,word):
            return word in self.words

    # pylint: disable=R0903
    class StrengthResult:
        def __init__(self,strength:str,score:int,feedback:str):
            self.strength = strength
            self.score = score
            self.feedback = feedback

class PasswordStrength:

    def __init__(self, weak_wordlist_path: str = "./weak_passwords.txt",
        banned_wordlist_path: str = "./banned_passwords.txt"):
        self.weak_wordlist = (Wordlist(weak_wordlist_path)
            if weak_wordlist_path else None)
        self.banned_wordlist = (Wordlist(banned_wordlist_path)
            if banned_wordlist_path else None)
        self.min_password_length = 12
        self.strength_mapping = {
            0: "Very Weak",
            1: "Weak",
            2: "Moderate",
            3: "Strong",
            4: "Very Strong"

        }

    @lru_cache(maxsize=1000)
    def check_password_strength(self, password: str) :
        """Check the strength of a given password."""
        if len(password) < self.min_password_length:
            return StrengthResult("Too short", 0, "Password should be at least 12 characters long.")

        if self.weak_wordlist and self.weak_wordlist.is_word_in_list(password):
            return StrengthResult("Weak", 0, "Password is commonly used and easily guessable.")

        if self.banned_wordlist and self.banned_wordlist.is_word_in_list(password):
            return StrengthResult("Banned", 0,
                "This password is not allowed, as it is commonly found in data leaks.")





