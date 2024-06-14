import os
from openai import OpenAI

# Configuration settings for the File Organization application

# Directly set the OpenAI API key
OPENAI_API_KEY = ''

# Instantiate the OpenAI client with the API key
client = OpenAI(api_key=OPENAI_API_KEY)

# Default path for the directory to organize (can be overridden in the GUI)
DEFAULT_DIRECTORY = r'C:\Users\ArteZan\Desktop'

# Add any additional configurations here
# For example, you can define default categorization rules, logging settings, etc.
