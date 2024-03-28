import gspread
import httplib2
import logging

import sys
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
sheet_id = os.getenv("SHEET_ID")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class GoogleSheetsApiAuth:
    @staticmethod
    def get_google_services() -> tuple[gspread.Client, build]:
        """ Returns gspread client object and Google Sheets API service using service account credentials """

        creds_json = os.path.join(os.path.dirname(__file__), "credentials.json")
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes)
        creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
        service = build('sheets', 'v4', http=creds_service)
        client = gspread.authorize(credentials)

        return client, service

    @staticmethod
    def get_sheet(spreadsheet: gspread.Worksheet) -> tuple[list[list[str]], list[str], list[str]]:
        """ GET whole cells from table """

        data = spreadsheet.get_all_values()

        # # GET 'Ref' Row
        ref_column = [row[0] for row in data[1:]]

        # GET 'Type' Row
        type_column = [row[9] for row in data[1:]]

        return data, ref_column, type_column
