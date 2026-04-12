import gspread
from google.oauth2.service_account import Credentials


class GoogleSheetsClient:
    def get_client(self, credentials_file):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_file(
            credentials_file, scopes=scopes
        )
        return gspread.authorize(credentials)

    def get_spreadsheet(self, client, spreadsheet):
        return client.open(spreadsheet)

    def get_worksheets(self, spreadsheet):
        return spreadsheet.worksheets()