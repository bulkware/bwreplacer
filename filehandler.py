# !/usr/bin/env python3
# -*- coding: utf-8 -*-

""" A class to handle files. """

# Imports
import os # Miscellaneous operating system interfaces
import re # Regular expression operations
import sys # System-specific parameters and functions

# A class to handle files
class FileHandler(object):

    # Initialization
    def __init__(self, filetypes):

        # Declare class variables
        self.error = "" # String for errors
        self.filepath = None # File path
        self.filetype = None # File type
        self.filetypes = filetypes # Accepted file types
        self.data = {} # Data-dictionary


    # Close
    def close(self):
        self.error = ""
        self.filepath = None
        self.filetype = None
        self.data = {}


    # Return the number of lines
    def count(self):

        # Clear error message
        self.error = ""

        # Check for file
        if not self.filepath:
            self.error = "No file open."
            return False

        return len(self.data)


    # Return only data we want to process
    def get_editdata(self):

        # Clear error message
        self.error = ""

        # Check for file
        if not self.filepath:
            self.error = "No file open."
            return False

        # If the file is an .srt-file
        if self.filetype == "srt":

            # Dictionary
            filedata = {}

            # Regular expression to match timecodes
            timecode = "^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\Z"

            # Loop through filedata-dictionary and discard unwanted lines 
            for key in self.data:

                # Line variable to make this easier
                line = self.data[key]

                # Separate actual subtitle lines
                if line == "": # Empty line
                    continue
                elif line.isdigit(): # Subtitle line number
                    continue
                elif re.match(timecode, line): # Subtitle timecode
                    continue
                else: # Add line
                    filedata[key] = line

            # Return dictionary
            return filedata

        # If the file is a .txt-file
        elif self.filetype == "txt":

            # Dictionary
            filedata = {}

            # Loop through filedata-dictionary and discard unwanted lines 
            for key in self.data:

                # Line variable to make this easier
                line = self.data[key]

                # Separate actual lines
                if line == "": # Empty line
                    continue
                else: # Add line
                    filedata[key] = line

            # Return dictionary
            return filedata


    # Return the whole file
    def get_filedata(self):

        # Clear error message
        self.error = ""

        # Check for file
        if not self.filepath:
            self.error = "No file open."
            return False

        # Return dictionary
        return self.data


    # Return specific line from file
    def get_line(self, key):

        # Clear error message
        self.error = ""

        # Check for file
        if not self.filepath:
            self.error = "No file open."
            return False

        return self.data[key]


    # Replace specific line to file
    def set_line(self, key, line):

        # Clear error message
        self.error = ""

        # Check for file
        if not self.filepath:
            self.error = "No file open."
            return False

        # Only apply if the line has changed
        if self.data[key] != line:
            self.data[key] = line

        return True


    # Open file
    def open(self, file, enc):

        # Clear error message
        self.error = ""

        # Close any previous file
        self.close()

        # Check file path
        if file == "":
            self.error = "Filename is empty."
            return False

        # Check if file exists
        if not os.path.exists(file):
            self.error = "File does not exist: " + file
            return False

        # File path should be an existing regular file
        if not os.path.isfile(file):
            self.error = "Not a file: " + file
            return False

        # File should not be empty
        if not os.path.getsize(file) > 0:
            self.error = "File is empty: " + file
            return False

        # Check file extension
        ext = os.path.splitext(file)[1][1:].lower()
        if ext not in self.filetypes:
            self.error = "File type is not valid: " + file
            return False

        # Loop through file and set file data into a dictionary
        try:
            filehandle = open(file, "r", encoding=enc)
            i = 0
            while True:
                line = filehandle.readline()
                if len(line) == 0: # Zero lenght indicates EOF
                    break
                line = line.rstrip("\r\n")
                self.data[i] = line
                i += 1
            filehandle.close()
        except IOError as e:
            self.error = "I/O error({0}): {1}".format(e.errno, e.strerror)
            return False
        except UnicodeDecodeError:
            self.error = "Unicode Decode Error: " + file
            return False
        except UnicodeEncodeError:
            self.error = "Unicode Encode Error: " + file
            return False
        except:
            self.error = "Unexpected error: " + str(sys.exc_info()[1])
            return False
        else:
            self.filepath = file
            self.filetype = ext
            return True


    # Save file
    def save(self, enc, emptylines):

        # Clear error message
        self.error = ""

        # Check for file
        if not self.filepath:
            self.error = "No file open."
            return False

        # Remove empty lines from the end of the file
        if emptylines:
            while len(self.data) > 1 and self.data[len(self.data) - 1] == "":
                del self.data[len(self.data) - 1]

        # Loop dictionary and save to file
        try:
            filehandle = open(self.filepath, "w", encoding=enc)
            for key, value in sorted(self.get_filedata().items()):
                filehandle.write(value + "\n")
            filehandle.close()
        except IOError as e:
            self.error = "I/O error({0}): {1}".format(e.errno, e.strerror)
            return False
        except UnicodeDecodeError:
            self.error = "Unicode Decode Error: " + self.filepath
            return False
        except UnicodeEncodeError:
            self.error = "Unicode Encode Error: " + self.filepath
            return False
        except:
            self.error = "Unexpected error: " + str(sys.exc_info()[1])
            return False
        else:
            return True
