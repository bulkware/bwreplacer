# !/usr/bin/env python3
# -*- coding: utf-8 -*-

""" A class for easier data access """

# Imports
import os # Miscellaneous operating system interfaces
import sqlite3 # DB-API 2.0 interface for SQLite databases

# A class for easier data access
class DataHandler(object):

    # Initialization
    def __init__(self):

        # Declare variables
        self.correctionmodes = ["All", "RegEx", "Replace", "Word"] # Modes
        self.error = "" # String for errors
        self.database = None # Database name
        self.rowid = 0 # Row ID


    # Open database
    def open(self, filepath):

        # Check file path
        if not filepath:
            self.error = "Database file path is not valid."
            return False

        # Check if file path is empty
        if filepath == "":
            self.error = "Database file path is empty."
            return False

        # File path should be an existing regular file
        if not os.path.isfile(filepath):
            self.error = "Database file path is not a file."
            return False

        # Check file extension
        ext = os.path.splitext(filepath)[1][1:].lower()
        if ext != "db":
            self.error = "Database file extension is not valid."
            return False

        # Fetch appinfo
        try:
            connection = sqlite3.connect(filepath)
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM appinfo WHERE id=1")
            name = cursor.fetchone()
            connection.close()
            if name[0] != "bwReplacer":
                self.database = None
                self.error = "Not a valid database: " + filepath
                return False
        except:
            self.database = None
            self.error = "Unable to open database: " + filepath
            return False
        else:
            self.database = filepath
            return True


    # Count rows
    def count(self, table):

        # Check for database
        if not self.database:
            self.error = "No database opened."
            return False

        try:
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()

            # Check if table exists
            query = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND \
                name='%s'" % (table)
            cursor.execute(query)
            tablecount = int(cursor.fetchone()[0])
            if tablecount < 1:
                self.error = "Table does not exist in database: " + table
                return False

            # Count table rows
            query = "SELECT COUNT(*) FROM '%s'" % (table)
            cursor.execute(query)
            count = int(cursor.fetchone()[0])
            connection.close()
        except:
            return False
        else:
            return count


    # Create a new database
    def create_database(self, name):

        # Empty the error message string
        self.error = ""

        # Check against an empty name
        if name == "":
            self.error = "Database name cannot be empty."
            return False

        # Add extension if necessary
        if not name.endswith(".db"):
            name += ".db"

        # Check if file already exists
        if os.path.isfile(name):
            self.error = "Database with that name already exists."
            return False

        self.database = None

        # Try to create, connect and set up database
        try:
            connection = sqlite3.connect(name)
            cursor = connection.cursor()

            # Create tables
            cursor.execute("CREATE TABLE appinfo (id INTEGER PRIMARY KEY \
                AUTOINCREMENT, name TEXT)")
            cursor.execute("CREATE TABLE lists (id INTEGER PRIMARY \
                KEY AUTOINCREMENT, selected INT, name TEXT, \
                comment TEXT)")
            cursor.execute("CREATE TABLE corrections (id INTEGER PRIMARY KEY \
                AUTOINCREMENT, mode INT, list INT, variations INT, error TEXT, \
                correction TEXT, comment TEXT)")
            cursor.execute("INSERT INTO appinfo (name) VALUES ('bwReplacer')")
            connection.commit()
        except:
            self.database = None
            self.error = "Unable to setup database tables."
            return False
        else:
            self.database = name
            connection.close()
            return True


    # Delete row
    def delete(self, id, table):

        # Check for database
        if not self.database:
            self.error = "No database opened."
            return False

        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        # Execute SQL-query based on table
        if table == "lists":
            cursor.execute("DELETE FROM lists WHERE id=?", \
                (int(id),))
        elif table == "corrections":
            cursor.execute("DELETE FROM corrections WHERE id=?", (int(id),))
        else:
            self.error = "Unknow table: " + table
            return False

        # Check if any rows were affected
        if cursor.rowcount < 1:
            self.error = "Row does not exist. ID: " + str(id)
            return False

        # Commit changes and close connection
        connection.commit()
        connection.close()
        return True


    # Get correction
    def get_correction(self, id=None, name=None):

        # Check for database
        if not self.database:
            self.error = "No database opened."
            return False

        # Fetch list by id or name
        try:
            if id:
                id = int(id)
                query = "SELECT * FROM corrections WHERE id=%s" % (id)
            elif name:
                name = str(name)
                query = "SELECT * FROM corrections WHERE name='%s'" % (name)
            else:
                return None

            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()
            cursor.execute(query)
            list = cursor.fetchone()
            connection.close()
        except:
            return None
        else:
            return list


    # Get corrections
    def get_corrections(self, modes, lists):

        # Check for database
        if not self.database:
            self.error = "No database opened."
            return False

        # Check for modes
        if not modes:
            return

        # Check for lists
        if not lists:
            return

        try:
            modes = ",".join(map(str, modes))
            lists = ",".join(map(str, lists))
            query = "SELECT * FROM corrections WHERE mode IN (%s) AND \
                list IN (%s) ORDER BY mode,error" % (modes, lists)
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            connection.close()
        except:
            return
        else:
            return rows


    # Get list
    def get_list(self, id=None, index=None):

        # Check for database
        if not self.database:
            self.error = "No database opened."
            return False

        # Fetch list by id or name
        try:
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()

            if id != None:
                id = int(id)
                query = "SELECT * FROM lists WHERE id=%s" % (id)
                cursor.execute(query)
                list = cursor.fetchone()
            elif index != None:
                index = int(index)

                query = "SELECT * FROM lists ORDER BY id"
                cursor.execute(query)
                rows = cursor.fetchall()

                list = None
                for i, row in enumerate(rows):
                    if index == i:
                        list = row
            else:
                return None
        except:
            connection.close()
            return None
        else:
            connection.close()
            return list


    # Get lists
    def get_lists(self):

        # Check for database
        if not self.database:
            self.error = "No database opened."
            return False

        try:
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()
            query = "SELECT * FROM lists ORDER BY id"
            cursor.execute(query)
            rows = cursor.fetchall()
            connection.close()
        except:
            return None
        else:
            return rows


    # Insert row
    def insert(self, table, values):

        self.error = ""

        # Check for database
        if not self.database:
            self.error = "No database opened."
            return False

        try:
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()

            # Execute SQL-query based on table
            if table == "lists":
                cursor.execute("INSERT INTO lists (selected, name, comment) \
                    VALUES (?, ?, ?)", (int(values[0]), str(values[1]), \
                    str(values[2])))
            elif table == "corrections":
                cursor.execute("INSERT INTO corrections (mode, \
                    list, variations, error, correction, comment) VALUES \
                    (?, ?, ?, ?, ?, ?)", (int(values[0]), int(values[1]), \
                    int(values[2]), str(values[3]), str(values[4]), \
                    str(values[5])))
            else:
                self.error = "Unknow table: " + table
                return False

            self.rowid = int(cursor.lastrowid)

            # Commit changes and close connection
            connection.commit()
            connection.close()
        except:
            self.message = "Unable to insert row to database table: " + table
            return False
        else:
            return True

    # Update row
    def update(self, table, values):

        # Check for database
        if not self.database:
            self.error = "No database opened."
            return False

        try:
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()

            # Execute SQL-query based on table
            if table == "lists":
                cursor.execute("UPDATE lists SET selected=?, name=?, comment=? \
                    WHERE id=?", (int(values[1]), str(values[2]), \
                    str(values[3]), int(values[0])))
            elif table == "corrections":
                cursor.execute("UPDATE corrections SET mode=?, list=?, \
                    variations=?, error=?, correction=?, comment=? \
                    WHERE id=?", (int(values[1]), int(values[2]), \
                    int(values[3]), str(values[4]), str(values[5]), \
                    str(values[6]), int(values[0])))
            else:
                self.error = "Unknow table: " + table
                return False

            # Commit changes and close connection
            connection.commit()
            connection.close()
        except:
            self.message = "Unable to update row in database table: " + table
            return False
        else:
            return True
