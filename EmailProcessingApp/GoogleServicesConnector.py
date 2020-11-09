from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.labels',
'https://www.googleapis.com/auth/gmail.readonly',
'https://www.googleapis.com/auth/gmail.settings.basic',
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/tasks',
'https://www.googleapis.com/auth/drive']

SPREADSHEET_NAME = 'EmailProcessing'

class GoogleServicesConnector():
    """This class does the authorization and discovery for
        the Google APIs that are being used"""

    def __init__(self):
        super(GoogleServicesConnector, self).__init__()
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def getGoogleDriveService(self):
        return build('drive', 'v3', credentials=self.creds)

    def getGoogleSheetsService(self):
        return build('sheets', 'v4', credentials=self.creds)

    def getGoogleMailService(self):
        return build('gmail', 'v1', credentials=self.creds)

    def getGoogleTasksService(self):
        return build('tasks', 'v1', credentials=self.creds)
