# !/usr/bin/env python3
# -*- coding: utf-8 -*-

""" An application to correct spelling errors from files. """

# Python imports
import os # Miscellaneous operating system interfaces
import re # Regular expression operations
import sys # System-specific parameters and functions

# Import PyQt modules
from PyQt4 import QtCore, QtGui

# Application classes
from datahandler import DataHandler # A class for easier data access
from filehandler import FileHandler # A class to handle files
from stringhandler import StringHandler # A class to perform string operations

# Import mainwindow
from mainwindow import *

# Create a class for our mainwindow
class Main(QtGui.QMainWindow):

    # Initialize mainwindow
    def __init__(self):

        # Initialize top level window widget
        QtGui.QMainWindow.__init__(self)

        # Declare class variables
        self.encodings = [
            ["Default", None],
            ["ASCII", "ascii"],
            ["ISO-8859-1", "latin_1"],
            ["ISO-8859-2", "iso8859_2"],
            ["ISO-8859-3", "iso8859_3"],
            ["ISO-8859-4", "iso8859_4"],
            ["ISO-8859-5", "iso8859_5"],
            ["ISO-8859-6", "iso8859_6"],
            ["ISO-8859-7", "iso8859_7"],
            ["ISO-8859-8", "iso8859_8"],
            ["ISO-8859-9", "iso8859_9"],
            ["ISO-8859-10", "iso8859_10"],
            ["ISO-8859-13", "iso8859_13"],
            ["ISO-8859-14", "iso8859_14"],
            ["ISO-8859-15", "iso8859_15"],
            ["KOI8-R", "koi8_r"],
            ["KOI8-U", "koi8_u"],
            ["UTF-8", "utf_8_sig"],
            ["UTF-8 without BOM", "utf_8"],
            ["UTF-16BE", "utf_16_be"],
            ["UTF-16LE", "utf_16_le"],
            ["UTF-32BE", "utf_32_be"],
            ["UTF-32LE", "utf_32_le"],
            ["Windows-1250", "cp1250"],
            ["Windows-1251", "cp1251"],
            ["Windows-1252", "cp1252"],
            ["Windows-1253", "cp1253"],
            ["Windows-1254", "cp1254"],
            ["Windows-1255", "cp1255"],
            ["Windows-1256", "cp1256"],
            ["Windows-1257", "cp1257"],
            ["Windows-1258", "cp1258"]
        ]
        self.dirpath = "" # Directory path for batch fix
        self.filepath = "" # File path for fix
        self.filelist = [] # File list for batch fix
        self.filetypes = ["srt", "txt"] # Accepted file types
        self.typefilter = "All supported files (*.srt *.txt)"
        self.typefilter += ";;SubRip subtitle file (*.srt)"
        self.typefilter += ";;Text file (*.txt)"

        # Create class instances
        self.data = DataHandler()
        self.file = FileHandler(self.filetypes)
        self.string = StringHandler()

        # This is always the same
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals, menu
        QtCore.QObject.connect(self.ui.actionCreateDatabase,
            QtCore.SIGNAL('triggered()'), self.createDatabase)
        QtCore.QObject.connect(self.ui.actionOpenDatabase,
            QtCore.SIGNAL('triggered()'), self.openDatabase)
        QtCore.QObject.connect(self.ui.actionQuit,
            QtCore.SIGNAL('triggered()'), self.quitApplication)
        QtCore.QObject.connect(self.ui.actionWiki,
            QtCore.SIGNAL('triggered()'), self.wikiLink)
        QtCore.QObject.connect(self.ui.actionAbout,
            QtCore.SIGNAL('triggered()'), self.aboutMessage)

        # Connect signals, buttons
        QtCore.QObject.connect(self.ui.btnFOpenFile,
            QtCore.SIGNAL('clicked()'), self.fOpenFile)
        QtCore.QObject.connect(self.ui.btnFStart,
            QtCore.SIGNAL('clicked()'), self.fStart)

        QtCore.QObject.connect(self.ui.btnBFStart,
            QtCore.SIGNAL('clicked()'), self.bfStart)
        QtCore.QObject.connect(self.ui.btnBFOpenDir,
            QtCore.SIGNAL('clicked()'), self.bfOpenDir)

        QtCore.QObject.connect(self.ui.btnLDeleteRow,
            QtCore.SIGNAL('clicked()'), self.lDeleteRow)
        QtCore.QObject.connect(self.ui.btnLInsertRow,
            QtCore.SIGNAL('clicked()'), self.lInsertRow)
        QtCore.QObject.connect(self.ui.btnLUpdateRow,
            QtCore.SIGNAL('clicked()'), self.lUpdateRow)

        QtCore.QObject.connect(self.ui.btnCDeleteRow,
            QtCore.SIGNAL('clicked()'), self.cDeleteRow)
        QtCore.QObject.connect(self.ui.btnCInsertRow,
            QtCore.SIGNAL('clicked()'), self.cInsertRow)
        QtCore.QObject.connect(self.ui.btnCUpdateRow,
            QtCore.SIGNAL('clicked()'), self.cUpdateRow)

        # Connect signals, comboboxes
        QtCore.QObject.connect(self.ui.cboCCorrectionMode,
            QtCore.SIGNAL('activated(QString)'), self.refreshCCorrections)
        QtCore.QObject.connect(self.ui.cboCList,
            QtCore.SIGNAL('activated(QString)'), self.refreshCCorrections)

        # Connect signals, tables
        QtCore.QObject.connect(self.ui.tblCCorrections,
            QtCore.SIGNAL('currentCellChanged(int,int,int,int)'),
            self.selectCorrection)

        # Loop and set encodings to settings combobox
        for item in self.encodings:
            self.ui.cboSFileEncoding.addItem(item[0])

        # Select the first tab from the tab widgets
        self.ui.tabMain.setCurrentIndex(0)

        # Load settings
        settings = QtCore.QSettings("bulkware", "bwReplacer")
        if settings.contains("database"):
            file = settings.value("database")

            # Try to connect to the database
            ok = self.data.open(file)
            if ok:
                self.refreshLists()
                self.refreshLLists()
                self.refreshCCorrections()
                self.enableWidgets()
                msg = "Successfully connected to database: " + str(file)
                self.ui.statusBar.showMessage(msg)
            else:
                msg = "Unable to connect to previous database."
                self.ui.statusBar.showMessage(msg)

        # Load setting: encoding
        if settings.contains("encoding"):
            self.ui.cboSFileEncoding.setCurrentIndex(settings.value("encoding",
                type=int))

        # Load setting: file
        if settings.contains("filepath"):
            self.filepath = settings.value("filepath", type=str)
            self.openFile(self.filepath)

        # Load setting: path
        if settings.contains("dirpath"):
            self.dirpath = settings.value("dirpath", type=str)
            self.openDir(self.dirpath)


    # Menu > File > Quit
    def quitApplication(self):
        QtGui.QApplication.quit()


    # Menu > File > Create a new database...
    def createDatabase(self):

        # Dialog for database name
        name, ok = QtGui.QInputDialog.getText(self, "Create a new database", 
            "Enter name for database:")

        if not ok:
            return

        if name == "":
            msg = "Database name cannot be empty."
            self.ui.statusBar.showMessage(msg)
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Disable widgets
        self.disableWidgets()

        try:
            self.data.create_database(name)
            self.refreshLists()
            self.refreshLLists()
            self.refreshCCorrections()
        except:
            msg = "Unable to create database."
            self.ui.statusBar.showMessage(msg)
            QtGui.QMessageBox.critical(self, "Error", msg)
            return False
        else:
            msg = "Database created: " + self.data.database
            self.ui.statusBar.showMessage(msg)

        # Enable widgets
        self.enableWidgets()


    # Menu > File > Open database...
    def openDatabase(self):

        # Get the database file using a dialog
        file = QtGui.QFileDialog.getOpenFileName(self, "Open database",
            os.path.dirname(sys.argv[0]), "SQLite databases (*.db)")

        # If the filename was not provided
        if file == "":
            return

        # Disable widgets
        self.disableWidgets()

        # Try to open database
        if not self.data.open(file):
            self.ui.statusBar.showMessage(self.data.error)
            QtGui.QMessageBox.critical(self, "Error", self.data.error)
            return

        # Refresh main window widgets
        self.refreshLists()
        self.refreshCCorrections()
        self.refreshLLists()

        # Enable widgets
        self.enableWidgets()

        # Show success msg
        msg = "Successfully opened database: " + file
        self.ui.statusBar.showMessage(msg)


    # Menu > Help > Wiki
    def wikiLink(self):
        address = "http://sourceforge.net/p/bwreplacer/wiki/"
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(address))


    # Menu > Help > About...
    def aboutMessage(self):
        msg = """<strong>bwReplacer</strong><br />
        Version 1.01<br />
        <br />
        This is free software.<br />
        Released under the General Public License.<br />
        <br />
        <a href="http://sourceforge.net/projects/bwreplacer">SourceForge</a>"""
        QtGui.QMessageBox.about(self, "About", msg)


    # Fix, open file
    def fOpenFile(self):

        # Get file using a dialog
        file = QtGui.QFileDialog.getOpenFileName(self, "Select file",
            self.filepath, self.typefilter)

        # Check if file string is not empty
        if file == "":
            return

        ok = self.openFile(file)
        if ok:
            msg = "File opened successfully."
            self.ui.statusBar.showMessage(msg)
        else:
            self.ui.statusBar.showMessage(self.file.error)
            QtGui.QMessageBox.critical(self, "Error", self.file.error)


    # Open file
    def openFile(self, file):

        # Get the file encoding setting
        enc = self.encodings[self.ui.cboSFileEncoding.currentIndex()][1]

        # Try to open file
        ok = self.file.open(file, enc)
        if not ok:
            return False

        # Put file path into class variable
        self.filepath = file

        # Put file data into widgets
        self.ui.txtFFile.setText(self.filepath)
        self.ui.lstFFileContents.clear()
        for key, value in self.file.get_filedata().items():
            self.ui.lstFFileContents.addItem(value)

        # Everything went well
        self.file.close()
        return True


    # Fix, start
    def fStart(self):

        # Check for database
        if not self.data.database:
            msg = "Database connection not established."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Create a list of selected lists
        lists = []
        for sel in range(self.ui.lstFLists.count()):
            if self.ui.lstFLists.item(sel).checkState():
                lists.append(self.data.get_list(index=sel)[0])

        # Check for lists
        if not lists:
            msg = "No lists defined."
            self.ui.statusBar.showMessage(msg)
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Get corrections
        corrections = self.data.get_corrections([1,2,3], lists)

        # Check for corrections
        if not corrections:
            msg = "No corrections to apply."
            self.ui.statusBar.showMessage(msg)
            QtGui.QMessageBox.critical(self, "Error", msg)
            return False

        # Disable widgets
        self.disableWidgets()

        # Fix file
        self.string.reset()
        ok, msg = self.fixFile(self.filepath, corrections)
        if ok:
            self.ui.statusBar.showMessage(msg)
        else:
            self.ui.statusBar.showMessage(msg)
            QtGui.QMessageBox.critical(self, "Error", msg)

        # Show statistics if processing went ok
        if ok:
            msg = "Processing finished. %s corrections were applied." % \
                (self.string.count)
            self.ui.statusBar.showMessage(msg)

        # Reload file
        ok = self.openFile(self.filepath)
        if not ok:
            self.ui.statusBar.showMessage(self.file.error)
            QtGui.QMessageBox.critical(self, "Error", self.file.error)

        # Enable widgets
        self.enableWidgets()


    # Batch fix, Select directory...
    def bfOpenDir(self):

        # Get directory using a dialog
        path = QtGui.QFileDialog.getExistingDirectory(self, \
            "Select directory", self.dirpath)

        # Check if path string is empty
        if path == "":
            return

        ok = self.openDir(path)
        if ok and self.filelist:
            msg = "Directory opened successfully."
            self.ui.statusBar.showMessage(msg)
        elif ok and not self.filelist:
            msg = "No files found from directory."
            self.ui.statusBar.showMessage(msg)
            QtGui.QMessageBox.critical(self, "Error", msg)
        else:
            msg = "Unable to open directory."
            self.ui.statusBar.showMessage(msg)
            QtGui.QMessageBox.critical(self, "Error", msg)


    # Open dir
    def openDir(self, path):

        # Check if path is indeed a directory and create filelist
        if not os.path.isdir(path):
            return False

        # Put path into class variable
        self.dirpath = path

        # Put dir data into widgets
        self.ui.txtBFDir.setText(self.dirpath)
        self.ui.lstBFFileList.clear()
        self.filelist = []
        for item in os.listdir(self.dirpath):
            file = os.path.join(self.dirpath, item)
            ext = os.path.splitext(item)[1][1:].lower()
            if os.path.isfile(file) and ext in self.filetypes:
                self.filelist.append(file)
                self.ui.lstBFFileList.addItem(item)

        # Everything went well
        return True


    # Batch fix, start
    def bfStart(self):

        # Check for database
        if not self.data.database:
            msg = "Database connection not established."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Create a list of selected lists
        lists = []
        for sel in range(self.ui.lstFLists.count()):
            if self.ui.lstFLists.item(sel).checkState():
                lists.append(self.data.get_list(index=sel)[0])

        # Check for lists
        if not lists:
            msg = "No lists defined."
            self.ui.statusBar.showMessage(msg)
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Get corrections
        corrections = self.data.get_corrections([1,2,3], lists)

        # Check for corrections
        if not corrections:
            msg = "No corrections to apply."
            self.ui.statusBar.showMessage(msg)
            QtGui.QMessageBox.critical(self, "Error", msg)
            return False

        # Disable widgets
        self.disableWidgets()

        # Loop file list
        self.string.reset()
        for file in self.filelist:
            ok, msg = self.fixFile(file, corrections)
            if ok:
                self.ui.statusBar.showMessage(msg)
            else:
                self.ui.statusBar.showMessage(msg)
                QtGui.QMessageBox.critical(self, "Error", msg)
                break

        # Show statistics if processing went ok
        if ok:
            msg = "Processing finished. %s corrections were applied." % \
                (self.string.count)
            self.ui.statusBar.showMessage(msg)

        # Enable widgets
        self.enableWidgets()


    # Fix file
    def fixFile(self, file, corrections):

        # Get the file encoding setting
        enc = self.encodings[self.ui.cboSFileEncoding.currentIndex()][1]

        # Open file
        if not self.file.open(file, enc):
            return False, self.file.error

        i = 1
        lines = self.file.count()

        # Loop file's editable data
        for key, line in sorted(self.file.get_editdata().items()):

            # Loop corrections
            for item in corrections:
                ok, line = self.string.replace(line, int(item[1]), \
                    str(item[4]), str(item[5]), int(item[3]))

                if not ok:
                    return False, self.string.error

            # Set corrected line back to file
            self.file.set_line(key, line)

            if i % 100 == 0:
                msg = "Processing file: %s (line %s/%s)" \
                    % (os.path.basename(file), key, lines)
                self.ui.statusBar.showMessage(msg)

                # Update app
                QtGui.QApplication.processEvents()

            i += 1

        # Check for empty lines at EOF removal option
        if self.ui.chkSRemoveEmpty.isChecked():
            emptylines = True
        else:
            emptylines = False

        # Save file
        if not self.file.save(enc, emptylines):
            return False, self.file.error

        # Close file
        self.file.close()

        # All went well
        return True, "File processed successfully: " + file


    # Refresh widgets with lists
    def refreshLists(self):

        # Check for database
        if not self.data.database:
            return

        # Clear widgets
        self.ui.cboCList.clear()
        self.ui.lstFLists.clear()
        self.ui.lstBFLists.clear()

        # Get lists
        lists = self.data.get_lists()

        # Check for lists
        if not lists:
            return

        # Set lists to widgets
        for list in lists:

            # Corrections
            self.ui.cboCList.addItem(list[2])

            # Fix, list
            item = QtGui.QListWidgetItem(list[2])
            item.setFlags(QtCore.Qt.ItemIsEnabled |
                QtCore.Qt.ItemIsUserCheckable)
            if list[1] == 1:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.lstFLists.addItem(item)

            # Batch fix, list
            item = QtGui.QListWidgetItem(list[2])
            item.setFlags(QtCore.Qt.ItemIsEnabled | 
                QtCore.Qt.ItemIsUserCheckable)
            if list[1] == 1:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.lstBFLists.addItem(item)


    # Refresh lists table
    def refreshLLists(self):

        # Check for database
        if not self.data.database:
            return

        # Clear lists table
        self.ui.tblLLists.setColumnCount(0)
        self.ui.tblLLists.setRowCount(0)
        self.ui.tblLLists.clear()

        # Get lists
        rows = self.data.get_lists()

        # Check for lists
        if not rows:
            return

        # Set columns and rows for table
        self.ui.tblLLists.setColumnCount(4)
        self.ui.tblLLists.setRowCount(len(rows))

        # Set header labels for table
        self.ui.tblLLists.setHorizontalHeaderLabels(["ID", "Selected", "Name", \
            "Comment"])

        # Populate table
        for i, row in enumerate(rows):
            for column in range(4):

                # Column 1 is the selected column
                if column == 1:
                    item = QtGui.QTableWidgetItem("Y/n")
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                        QtCore.Qt.ItemIsEnabled)
                    if row[column]:
                        item.setCheckState(QtCore.Qt.Checked)
                    else:
                        item.setCheckState(QtCore.Qt.Unchecked)
                else:
                    text = str(row[column])
                    item = QtGui.QTableWidgetItem(text)

                # ID column can't have any item flags
                if column == 0:
                    item.setFlags(QtCore.Qt.NoItemFlags)

                self.ui.tblLLists.setItem(i, column, item)

        # Set horizontal header visibility to true (QT BUG?)
        self.ui.tblLLists.horizontalHeader().setVisible(True)

        # Resize table columns to contents
        # setVisible lines are because of QTBUG-9352!
        self.ui.tblLLists.setVisible(False)
        self.ui.tblLLists.resizeColumnsToContents()
        self.ui.tblLLists.setVisible(True)


    # Delete list
    def lDeleteRow(self):

        # Check for database
        if not self.data.database:
            msg = "Database connection not established."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Check table's selected items
        if not self.ui.tblLLists.selectedIndexes():
            msg = "Please select item from table."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Get selected row
        row = int(self.ui.tblLLists.currentRow())

        # Get id
        id = int(self.ui.tblLLists.item(row, 0).text())

        # Delete list
        ok = self.data.delete(id, "lists")
        if ok:
            msg = "List deleted."
            self.ui.statusBar.showMessage(msg)
        else:
            self.ui.statusBar.showMessage(self.data.error)
            QtGui.QMessageBox.critical(self, "Error", self.data.error)
            return

        # Remove row from table
        self.ui.tblLLists.removeRow(row)


    # Insert list
    def lInsertRow(self):

        # Check for database
        if not self.data.database:
            msg = "Database connection not established."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Insert list
        ok = self.data.insert("lists", [0, "", ""])
        if ok:
            msg = "List inserted."
            self.ui.statusBar.showMessage(msg)
        else:
            self.ui.statusBar.showMessage(self.data.error)
            QtGui.QMessageBox.critical(self, "Error", self.data.error)
            return

        # Refresh the lists table
        self.refreshLLists()

        # Get the last row from table and insert new row
        lastrow = self.ui.tblLLists.rowCount() - 1

        # Select the name cell from the last row, which was inserted
        self.ui.tblLLists.setCurrentCell(lastrow, 3)
        self.ui.tblLLists.scrollToItem(
            self.ui.tblLLists.item(lastrow, 3),
            QtGui.QAbstractItemView.EnsureVisible)
        self.ui.tblLLists.setFocus()


    # Update list
    def lUpdateRow(self):

        # Check for database
        if not self.data.database:
            msg = "Database connection not established."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Check table's selected items
        if not self.ui.tblLLists.selectedIndexes():
            msg = "Please select item from table."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Get selected row
        row = int(self.ui.tblLLists.currentRow())

        # Get values
        id = int(self.ui.tblLLists.item(row, 0).text())
        selected = int(self.ui.tblLLists.item(row, 1).checkState())
        if selected > 1: selected = 1 # Tristate checkbox into 1
        name = str(self.ui.tblLLists.item(row, 2).text())
        comment = str(self.ui.tblLLists.item(row, 3).text())

        # Check if name is empty
        if name == "":
            msg = "Name cannot be the empty."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Update list
        ok = self.data.update("lists", [id, selected, name, comment])
        if ok:
            msg = "List updated."
            self.ui.statusBar.showMessage(msg)
        else:
            self.ui.statusBar.showMessage(self.data.error)
            QtGui.QMessageBox.critical(self, "Error", self.data.error)

        # Refresh lists
        self.refreshLists()
        self.refreshLLists()


    # Refresh corrections table
    def refreshCCorrections(self):

        # Clear corrections table
        self.ui.tblCCorrections.setColumnCount(0)
        self.ui.tblCCorrections.setRowCount(0)
        self.ui.tblCCorrections.clear()

        # Check for database
        if not self.data.database:
            return

        # Get lists
        lists = self.data.get_lists()

        # Check for lists
        if not lists:
            return

        # Mode
        modeid = int(self.ui.cboCCorrectionMode.currentIndex()) + 1
        modetext = str(self.data.correctionmodes[modeid])

        # List
        sel = int(self.ui.cboCList.currentIndex())
        listdata = self.data.get_list(index=sel)
        listid = int(listdata[0])
        listtext = str(listdata[2])

        # Get corrections
        rows = self.data.get_corrections([modeid], [listid])

        # Check for corrections
        if not rows:
            return

        # Set columns and rows for table
        self.ui.tblCCorrections.setColumnCount(7)
        self.ui.tblCCorrections.setRowCount(len(rows))

        # Set header labels for table
        self.ui.tblCCorrections.setHorizontalHeaderLabels(["ID", "Mode", \
            "List", "Variations", "Error", "Correction", "Comment"])

        # Populate corrections table
        for i, row in enumerate(rows):
            for column in range(7):

                if column == 0: # ID
                    text = str(row[column])
                    item = QtGui.QTableWidgetItem(text)
                    item.setFlags(QtCore.Qt.NoItemFlags)
                elif column == 1: # Mode
                    item = QtGui.QTableWidgetItem(modetext)
                elif column == 2: # List
                    item = QtGui.QTableWidgetItem(listtext)
                elif column == 3: # Variations
                    if row[column]:
                        text = "Yes"
                    else:
                        text = "No"
                    item = QtGui.QTableWidgetItem(text)
                else:
                    text = str(row[column])
                    item = QtGui.QTableWidgetItem(text)

                self.ui.tblCCorrections.setItem(i, column, item)


        # Set horizontal header visibility to true (QT BUG?)
        self.ui.tblCCorrections.horizontalHeader().setVisible(True)

        # Resize table columns to contents
        # setVisible lines are because of QTBUG-9352!
        self.ui.tblCCorrections.setVisible(False)
        self.ui.tblCCorrections.resizeColumnsToContents()
        self.ui.tblCCorrections.setVisible(True)


    # Select correction
    def selectCorrection(self, row, col, row2, col2):

        # Check if row is selected or row is not row2
        if row < 0 or row == row2:
            return

        # Get lists
        lists = self.data.get_lists()

        # Check for lists
        if not lists:
            return

        # Get ID and row data
        id = int(self.ui.tblCCorrections.item(row, 0).text())
        rowdata = self.data.get_correction(id)

        # Mode
        item = QtGui.QComboBox()
        item.addItems(self.data.correctionmodes[1:])
        item.setCurrentIndex(rowdata[1] - 1)
        self.ui.tblCCorrections.setCellWidget(row, 1, item)

        # List
        item = QtGui.QComboBox()
        for i, list in enumerate(lists):
            item.addItem(list[2])
            if list[0] == rowdata[2]:
                selectedlist = i
        item.setCurrentIndex(selectedlist)
        self.ui.tblCCorrections.setCellWidget(row, 2, item)

        # Variations
        item = QtGui.QTableWidgetItem("Y/n")
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        if int(rowdata[3]):
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)
        self.ui.tblCCorrections.setItem(row, 3, item)

        # Reset old row
        if row != row2 and row2 > -1:

            # Get ID and row data
            id = int(self.ui.tblCCorrections.item(row2, 0).text())
            rowdata = self.data.get_correction(id)

            # If there is no row data, the row was deleted
            if not rowdata:
                return

            # Mode
            modeid = int(rowdata[1])
            modetext = str(self.data.correctionmodes[modeid])
            self.ui.tblCCorrections.removeCellWidget(row2, 1)
            self.ui.tblCCorrections.setItem(row2, 1,
                QtGui.QTableWidgetItem(modetext))

            # List
            listid = int(rowdata[2])
            listtext = str(self.data.get_list(id=listid)[2])
            self.ui.tblCCorrections.removeCellWidget(row2, 2)
            self.ui.tblCCorrections.setItem(row2, 2,
                QtGui.QTableWidgetItem(listtext))

            # Variations
            if int(rowdata[3]):
                text = "Yes"
            else:
                text = "No"
            item = QtGui.QTableWidgetItem(text)
            self.ui.tblCCorrections.setItem(row2, 3, item)


    # Delete correction
    def cDeleteRow(self):

        # Check for database
        if not self.data.database:
            msg = "Database connection not established."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Check table's selected items
        if not self.ui.tblCCorrections.selectedIndexes():
            msg = "Please select item from table."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Get selected row
        row = int(self.ui.tblCCorrections.currentRow())

        # Get ID
        id = int(self.ui.tblCCorrections.item(row, 0).text())

        # Delete correction
        ok = self.data.delete(id, "corrections")
        if ok:
            msg = "Correction deleted, ID: %s" % (id)
            self.ui.statusBar.showMessage(msg)
        else:
            self.ui.statusBar.showMessage(self.data.error)
            QtGui.QMessageBox.critical(self, "Error", self.data.error)
            return

        # Remove row from table
        self.ui.tblCCorrections.removeRow(row)


    # Insert correction
    def cInsertRow(self):

        # Check for database
        if not self.data.database:
            msg = "Database connection not established."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Get lists
        lists = self.data.get_lists()

        # Check for lists
        if not lists:
            msg = "No lists defined."
            self.ui.statusBar.showMessage(msg)
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Mode
        modeid = int(self.ui.cboCCorrectionMode.currentIndex()) + 1
        modetext = str(self.data.correctionmodes[modeid])

        # List
        sel = int(self.ui.cboCList.currentIndex())
        listid = int(self.data.get_list(index=sel)[0])

        # Insert correction
        ok = self.data.insert("corrections", [modeid, listid, 0, "", "", ""])
        if ok:
            msg = "Row inserted."
            self.ui.statusBar.showMessage(msg)
        else:
            self.ui.statusBar.showMessage(self.data.error)
            QtGui.QMessageBox.critical(self, "Error", self.data.error)
            return

        # Refresh the corrections table
        self.refreshCCorrections()


    # Update correction
    def cUpdateRow(self):

        # Check for database
        if not self.data.database:
            msg = "Database connection not established."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Check table's selected items
        if not self.ui.tblCCorrections.selectedIndexes():
            msg = "Please select item from table."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Get lists
        lists = self.data.get_lists()

        # Check for lists
        if not lists:
            return

        # Get selected row
        row = int(self.ui.tblCCorrections.currentRow())

        # Get ID
        id = int(self.ui.tblCCorrections.item(row, 0).text())

        # Mode
        modeid = int(self.ui.tblCCorrections.cellWidget(row, 1).currentIndex())
        modeid += 1
        modetext = str(self.data.correctionmodes[modeid])

        # List
        sel = int(self.ui.tblCCorrections.cellWidget(row, 2).currentIndex())
        listdata = self.data.get_list(index=sel)
        listid = int(listdata[0])

        # Variations, error, correction and comment
        variations = int(self.ui.tblCCorrections.item(row, 3).checkState())
        if variations > 1: variations = 1 # Tristate checkbox into 1
        error = str(self.ui.tblCCorrections.item(row, 4).text())
        correction = str(self.ui.tblCCorrections.item(row, 5).text())
        comment = str(self.ui.tblCCorrections.item(row, 6).text())

        # Check if error is empty
        if error == "":
            msg = "Error cannot be the empty."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # Check if error and correction are the same
        if error == correction:
            msg = "Error and correction cannot be the same."
            QtGui.QMessageBox.critical(self, "Error", msg)
            return

        # If mode is RegEx, check for validity
        if modeid == 1:
            if not self.string.test(str(error), str(correction)):
                QtGui.QMessageBox.critical(self, "Error", self.string.error)
                return

        # Update correction
        ok = self.data.update("corrections", [id, modeid, listid, variations, \
            error, correction, comment])
        if ok:
            msg = "Correction updated."
            self.ui.statusBar.showMessage(msg)
        else:
            self.ui.statusBar.showMessage(self.data.error)
            QtGui.QMessageBox.critical(self, "Error", self.data.error)


    # Disable widgets
    def disableWidgets(self):
        self.ui.btnFOpenFile.setEnabled(False)
        self.ui.btnFStart.setEnabled(False)
        self.ui.btnBFOpenDir.setEnabled(False)
        self.ui.btnBFStart.setEnabled(False)
        self.ui.btnLDeleteRow.setEnabled(False)
        self.ui.btnLInsertRow.setEnabled(False)
        self.ui.btnLUpdateRow.setEnabled(False)
        self.ui.btnCDeleteRow.setEnabled(False)
        self.ui.btnCInsertRow.setEnabled(False)
        self.ui.btnCUpdateRow.setEnabled(False)


    # Enable widgets
    def enableWidgets(self):
        self.ui.btnFOpenFile.setEnabled(True)
        self.ui.btnFStart.setEnabled(True)
        self.ui.btnBFOpenDir.setEnabled(True)
        self.ui.btnBFStart.setEnabled(True)
        self.ui.btnLDeleteRow.setEnabled(True)
        self.ui.btnLInsertRow.setEnabled(True)
        self.ui.btnLUpdateRow.setEnabled(True)
        self.ui.btnCDeleteRow.setEnabled(True)
        self.ui.btnCInsertRow.setEnabled(True)
        self.ui.btnCUpdateRow.setEnabled(True)


    # Closing application
    def closeEvent(self, event):

        # Save settings
        settings = QtCore.QSettings("bulkware", "bwReplacer")
        settings.setValue("database", self.data.database)
        settings.setValue("encoding", self.ui.cboSFileEncoding.currentIndex())
        settings.setValue("filepath", self.filepath)
        settings.setValue("dirpath", self.dirpath)


# Creates an application object and begins the event handling loop
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    ret = app.exec_()
    sys.exit(ret)
