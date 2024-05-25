#!/usr/bin/env python
'''
Logic for securely gathering sensitive information from the user and writing
it to a .env file for use in the WallStreetBuzz application.

This module prompts the user for their Reddit API credentials and other
necessary configuration parameters, then writes these values to a .env file.
'''

# Built-in/Generic Imports
import os

__author__ = 'Austin Howard'
__copyright__ = 'Copyright 2024, Wallstreet Buzz'
__credits__ = ['Austin Howard']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Austin Howard'
__email__ = 'austin.d.howard@proton.me'
__status__ = 'prototype'


# Function to securely get sensitive information from user
def get_sensitive_info(prompt):
    """
    Prompts the user for sensitive information and ensures the input is not
    empty.

    Args:
        prompt (str): The prompt message displayed to the user.

    Returns:
        str: The user's input.
    """
    while True:
        value = input(prompt)
        if value.strip():  # Check if input is not empty
            return value


# Gather information from input
client_id = get_sensitive_info("Enter your client ID: ")
client_secret = get_sensitive_info("Enter your client secret: ")
user_agent = get_sensitive_info("Enter your user agent: ")
username = get_sensitive_info("Enter your Reddit username: ")
password = get_sensitive_info("Enter your Reddit password: ")

# Write information to a .env file
with open(".env", "w") as f:
    f.write(f"CLIENT_ID={client_id}\n")
    f.write(f"CLIENT_SECRET={client_secret}\n")
    f.write(f"USER_AGENT={user_agent}\n")
    f.write(f"USERNAME={username}\n")
    f.write(f"PASSWORD={password}\n")
    f.write(f"MAX_POSTS=10\n")
    f.write(f"LOGGING_LEVEL=INFO\n")
    f.write(f"CONSOLE_LOGGING=True")
