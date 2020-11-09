# PythonGooglePlayarea
I want to play around with Python and integrating it with a few Google applications

So far I have gotten the following to work:
* Google Drive
* Google Mail
* Google Sheets
* Mongo DB
* Google Tasks

The email processing app also does the following
* Finds the spreadsheet titled EmailProcessing (using Drive)
  * If not found it creates it
* Finds the sheet on that spreadsheet titled "Run History"
  * If not found it creates it and adds headers
* Appends an entry on the run history sheet
