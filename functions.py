# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# A function to convert bytes into human readable sizes
def convert_bytes(size):

    """ A function to convert bytes into human readable sizes. """

    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffixindex = 0

    while size > 1024:
        suffixindex += 1 # Increment the index of the suffix
        size = size / 1024 # Apply the division
    size = str(round(size, 2)) + chr(32) + suffixes[suffixindex]

    return size
