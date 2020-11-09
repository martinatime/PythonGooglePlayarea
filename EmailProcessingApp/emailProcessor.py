from __future__ import print_function
from pprint import pprint
from datetime import datetime
import GoogleServicesConnector

SPREADSHEET_NAME = 'EmailProcessing'
HISTORY_SHEET_NAME = 'Run History'

def main():
    """Process some emails and put details into a spreadsheet
    """
    google_api = GoogleServicesConnector.GoogleServicesConnector()

    drive_service = google_api.getGoogleDriveService()
    sheets_service = google_api.getGoogleSheetsService()
    gmail_service = google_api.getGoogleMailService()
    tasks_service = google_api.getGoogleTasksService()

    spreadsheetId = findOrCreateSpreadsheet(drive_service, sheets_service)

    now = datetime.now()
    appendRunHistory(sheets_service, spreadsheetId, str(now), 'test')

def initializeRunHistory(sheets_service, spreadsheetId, sheetName):
    historySheetId = findSheet(sheets_service, spreadsheetId, HISTORY_SHEET_NAME)
    if historySheetId is None:
        createSheet(sheets_service, spreadsheetId, HISTORY_SHEET_NAME)

def createSheet(sheets_service, spreadsheetId, sheetName):
    requests = []
    requests.append({
        "addSheet": {
            "properties": {
                "title": sheetName
            }
        }
    })
    body = {
        'requests': requests
    }
    response = sheets_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=body).execute()
    addHistoryHeader(sheets_service, spreadsheetId)

def addHistoryHeader(sheets_service, spreadsheetId):
    appendRunHistory(sheets_service, spreadsheetId, 'Timestamp', 'History Log Entry')

def appendRunHistory(sheets_service, spreadsheetId, time, log):
    values = [[time, log]]
    range = "'" + HISTORY_SHEET_NAME + "'!A1:B1"
    body = {
        'values': values
    }
    result = sheets_service.spreadsheets().values().append(spreadsheetId=spreadsheetId,range=range,valueInputOption='USER_ENTERED', body=body).execute()

def findSheet(sheets_service, spreadsheetId, sheetName):
    ranges = []
    include_grid_data = False
    request = sheets_service.spreadsheets().get(spreadsheetId=spreadsheetId, ranges=ranges, includeGridData=include_grid_data)
    response = request.execute()
    for sheet in response["sheets"]:
        if (sheet["properties"]["title"] == sheetName):
            return sheet["properties"]["sheetId"]

def findOrCreateSpreadsheet(drive_service, sheets_service):
    spreadsheetId = findSpreadsheet(drive_service)
    if spreadsheetId is not None:
        return spreadsheetId
    else:
        return createSpreadsheet(sheets_service)

def findSpreadsheet(drive_service):
    response = drive_service.files().list(q="name='" + SPREADSHEET_NAME + "'",spaces="drive").execute()
    for file in response.get('files', []):
        return file.get('id')

def createSpreadsheet(sheets_service):
    spreadsheet = {
        'properties' : {
            'title' : SPREADSHEET_NAME
        }
    }
    spreadsheet = sheets_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    return spreadsheet.get('spreadsheetId')

if __name__ == '__main__':
    main()
