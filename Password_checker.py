import tkinter as tk # GUI library for creating the application interface
from tkinter import filedialog, messagebox
import re # Regular expression module for password validation 
import random # Module for generating random passwords
import string # Module for string operations, used in password generation
import logging # Module for logging password check results
import json # Module for handling JSON data, used for saving password check results
import argparse # Module for parsing command-line arguments
import sys # Module for system-specific parameters and functions, used for exiting the application
from funtools import lru_cache # Module for caching results of expensive function calls, used for optimizing password strength checks
from zxcvbn import zxcvbn # Library for password strength estimation

