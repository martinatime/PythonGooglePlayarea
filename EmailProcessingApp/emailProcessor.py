from __future__ import print_function
import GoogleServicesConnector

SPREADSHEET_NAME = 'EmailProcessing'

def main():
    """Process some emails and put details into a spreadsheet
    """
    google_api = GoogleServicesConnector.GoogleServicesConnector()

    docs_service = google_api.getGoogleDocsService()
    sheets_service = google_api.getGoogleSheetsService()
    gmail_service = google_api.getGoogleMailService()

if __name__ == '__main__':
    main()
