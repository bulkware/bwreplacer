# !/usr/bin/env python3
# -*- coding: utf-8 -*-

""" A class to perform string operations """

# Python imports
import re # Regular expression operations

# A class to perform string operations
class StringHandler(object):

    # Initialization
    def __init__(self):

        # Declare variables
        self.count = 0 # Replace operation counter
        self.error = "" # String for errors


    # Replace 
    def replace(self, s, mode, old, new, variations=False):

        self.error = ""

        # Check if string is empty
        if s == "":
            self.error = "String is empty."
            return False, s

        # Check mode range
        if mode < 1 or mode > 3:
            self.error = "Mode is out of range."
            return False, s

        # Check if old and new match
        if old == new:
            self.error = "Old and new strings match."
            return False, s

        try:

            # RegEx
            if mode == 1: # RegEx
                s, c = re.subn(old, new, s)
                #self.count += c
                return True, s

            # Normal replace
            if s.find(old) > -1:
                if mode == 2: # Replace
                    self.count += s.count(old)
                    s = s.replace(old, new)
                elif mode == 3: # Word
                    s, c = re.subn(r"\b" + re.escape(old) + r"\b", new, s)
                    self.count += c

            # Should text case variations be performed?
            if not variations:
                return True, s

            # Capitalize
            oldc = old.capitalize()
            if old != oldc and s.find(oldc) > -1:
                if mode == 2: # Replace
                    self.count += s.count(oldc)
                    s = s.replace(oldc, new.capitalize())
                elif mode == 3: # Word
                    s, c = re.subn(r"\b" + re.escape(oldc) + r"\b", \
                        new.capitalize(), s)
                    self.count += c

            # Lowercase
            oldl = old.lower()
            if old != oldl and s.find(oldl) > -1:
                if mode == 2: # Replace
                    self.count += s.count(oldl)
                    s = s.replace(oldl, new.lower())
                elif mode == 3: # Word
                    s, c = re.subn(r"\b" + re.escape(oldl) + r"\b", \
                        new.lower(), s)
                    self.count += c

            # Uppercase
            oldu = old.upper()
            if old != oldu and s.find(oldu) > -1:
                if mode == 2: # Replace
                    self.count += s.count(oldu)
                    s = s.replace(oldu, new.upper())
                elif mode == 3: # Word
                    s, c = re.subn(r"\b" + re.escape(oldu) + r"\b", \
                        new.upper(), s)
                    self.count += c

        except re.error as e:
            self.error = "Regular expression error: " + str(e)
            return False, s
        except:
            self.error = "Unexpected error: " + str(sys.exc_info()[1])
            return False, s
        else:
            return True, s


    # Reset
    def reset(self):
        self.count = 0
        self.error = ""