# bwreplacer

An application to correct spelling errors from files. You can create your own
database with lists of corrections to search-and-replace strings from files.
Replace errors from multiple files with a single click of a button. Apply new
corrections to your database and apply those into different set of files.


## Corrections - Modes

### RegEx
In computing, a regular expression (abbreviated regex or regexp) is a sequence
of characters that forms a search pattern, mainly for use in pattern matching
with strings, or string matching, i.e. "find and replace"-like operations."
[Wikipedia - Regular expressions](http://en.wikipedia.org/wiki/Regular_expression

### Replace
A simple search-and-replace. Almost every text editor has the same feature.

### Word
A mode to distinguish words in lines. This is the most used mode in the
application. Basically it's the RegEx mode with the word boundaries surrounding
the error string. For example, if you would like to replace all the letters
`"l"` with the letter `"I"` (very common error when using
[OCR](http://en.wikipedia.org/wiki/Optical_character_recognition)), you should
use the "Word" mode. If you would use, say, the mode "Replace", the application
would replace all the letters `"l"`, including the ones inside words.
`"Shallow"` would become `"ShaIIow"`.

Note: The first and last characters of your error string should be alphanumeric
characters. Otherwise the mode does not work as expected. As explained above,
word boundaries are applied to the error string when fixing. This prevents you
from using any other characters than alphanumeric characters at the beginning
and the end of your error string, since the application is expecting a word
character at those positions. More technical explanation can be found at this
website: [http://www.regular-expressions.info/](http://www.regular-expressions.info/wordboundaries.html)


## Corrections - Variations

Since case-insensitive search-and-replace would bring it's own problems, the
application is provided with an option named "Variations". When enabled, this
option automatically creates different text-case variations of your error and
correction strings. For instance, error `"lor em"` and correction "lorem"
would have these variations:
`lor em --> lorem`
`Lor em --> Lorem`
`LOR EM --> LOREM`


## Menu commands

### File > Create a new database...
Create a new database.

### File > Open database
Opens a database.

### File > Quit
Quits the application.

### Help > Wiki (online)
Opens your web browser and takes you to the wiki page.

### Help > About...
Application information.


## Tabs - Batch fix

"Process multiple files."

### Path
The directory path to the files to process.

### Open directory...
Opens a directory.

### File list
List of files in the selected directory.

### Lists
Correction lists to use when processing files.

### Start
Starts the processing of the files.


## Tabs - Corrections

"Maintain the corrections in the database."

### Corrections (table)
ID = Key for the correction in database.
Mode = Mode of the correction when processing.
List = List of the correction.
Variations = Creates different text-case variations of your error and correction
    strings.
Error = The string to search when processing.
Correction = The string to apply when processing.
Comment = Comment for the correction.

### Mode
Filters the corrections from the database by selected mode.

### List
Filters the corrections from the database by selected list.

### Insert row
Inserts a new correction to the database.

### Delete row
Deletes the selected correction from the database.

### Update row
Applies the information of the selected correction to the database.


## Tabs - Fix

"Process a single file."

### File
The path to the file to process.

### Open file...
Opens a new file.

### File contents
The contents of the file.

### Lists
Correction lists to use when processing file.

### Start
Starts the file processing.


## Tabs - Lists

"Maintain the correction lists in the database."

### Lists (table)
ID = Key for the list in database.
Selected = Defines if the list should be selected by default when processing.
Name = Name of the list.
Comment = Comment for the list.

### Insert row
Inserts a new list to the database.

### Delete row
Deletes the selected list from the database.

### Update row
Applies the information of the selected list to the database.


## Tabs - Settings

"Modify the application's settings."

### File encoding
Specify the file encoding when opening and saving files. For more information
about file encodings, check the [wikipedia page](http://en.wikipedia.org/wiki/Character_encoding "Wikipedia - Character encoding").

### Remove empty lines from EOF
Removes the empty lines from the end of the file(s).


## Usage

### Opening a file
First you need to open a file. Currently the application supports two file
types, SubRip (srt) and text files (txt). Select the tab named "Fix" and click
the "Open file..." button. Browse for file using the windows open file dialog.

### Creating a new database
Select "Create a new database..." from the "File" menu. Enter a name for the
database and click "OK" on the dialog.

### Creating a correction list
Select the "Lists" tab. Click on the "Insert row" button. Now you have created
a new list for your corrections. Edit the name for the list you've created in
the "Name" column of the lists table and click "Update row" to save the changes
to the database.

### Creating a correction
Select the "Corrections" tab. Select the mode "Word" from the dropdown list on
the right. Right below should be the list you created on the "List" dropdown
menu. Now click on the "Insert row" button to create a new correction. Edit the
error and correction to the corrections table for your new correction. Click on
the "Update row" button to save the changes into the database. The error is the
string the program looks when you fix files and the correction is the
replacement string.

Now, let's assume the file you chose in the "Fix" tab has the word "lorem" in
it. If we would like to replace all those words to read "ipsum", we would create
a correction where the error would be "lorem" and the correction would be
"ipsum".

### Fixing a file
Return to the "Fix" tab. You should now still have your file loaded. Now click
on the "Start" button. Now all the corrections you have defined in the
"Corrections" tab are applied to the file.


## Running on Linux

### Installing dependencies (Debian-based systems)
Open your terminal application and type:
`sudo apt install python3 python3-pyqt4`

Hit enter. Enter your password when prompted. Answer yes to the question about
using additional disk space.

### Downloading the source
git clone https://github.com/bulkware/bwreplacer.git

### Running the application
Enter the application directory using this command:
`cd bwreplacer`

You can run the application from the source code using this command:
`python3 main.py`
