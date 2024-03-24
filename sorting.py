import gspread
import httplib2
import logging

import os

import time
from dotenv import load_dotenv
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
logging.basicConfig(level=logging.INFO)

sheet_id = os.getenv("SHEET_ID")

# To avoid limits and quotas on API requests
timeout = 5

colors = {
    "0": {"red": 201, "green": 218, "blue": 248},
    "2": {"red": 183, "green": 225, "blue": 205},
    "3": {"red": 87, "green": 187, "blue": 138},
    "13": {"red": 217, "green": 234, "blue": 211},
    "23": {"red": 234, "green": 209, "blue": 220},
}


class CellFormatter:
    """ Format cells bg-color/align"""

    @staticmethod
    def rgb_to_color(rgb: dict[str, int]) -> dict[str, float]:
        """ Converts RGB values to color format accepted by Google Sheets API """

        r = rgb.get("red") / 255
        g = rgb.get("green") / 255
        b = rgb.get("blue") / 255
        return {"red": r, "green": g, "blue": b}

    @staticmethod
    def color_by_type(service, ref_column: list[str], type_column: list[str], spreadsheet_id: str) -> None:
        """ Paint the cells background by Type """

        batch_requests = []

        # Iterate by ref_column | type_column
        for ref, type_value in zip(ref_column, type_column):
            type_value_str = str(type_value)

            # Check is color for this type exist
            if type_value_str in colors:

                # GET color for this type
                color = CellFormatter.rgb_to_color(colors[type_value_str])

                ref_rows_to_color = [i for i, ref_value in enumerate(ref_column, start=1) if ref_value == ref]
                for row in ref_rows_to_color:
                    row_index = row + 1
                    request = {
                        "repeatCell": {
                            "range": {
                                "sheetId": 0,
                                "startRowIndex": row_index - 1,
                                "endRowIndex": row_index,
                                "startColumnIndex": 0,
                                "endColumnIndex": 1
                            },
                            "cell": {
                                "userEnteredFormat": {
                                    "backgroundColor": color,
                                }
                            },
                            "fields": "userEnteredFormat.backgroundColor"
                        }
                    }
                    batch_requests.append(request)

        # Send all requests to update color in one batch
        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": batch_requests}).execute()


class CellSorter:
    @staticmethod
    def sort_data(data, ref_column: list[str]) -> list:
        """  Sort table by (ref_column) """
        sorted_data = [data[0]] + [row for _, row in sorted(zip(ref_column, data[1:]))]
        return sorted_data


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
        # GET whole cells from table
        data = spreadsheet.get_all_values()
        # logging.info(f"Data: {data}")

        # GET 'Ref' Row
        ref_column = [row[0] for row in data[1:]]

        # GET 'Type' Row
        type_column = [row[9] for row in data[1:]]

        return data, ref_column, type_column


class SheetUpdater:
    @staticmethod
    def update_sheet(service, sheet_id, sorted_data) -> None:
        """Updates the Google Sheets with sorted data"""

        # Generating queries to update cells in a table
        batch_requests = []
        for i, row in enumerate(sorted_data):
            row_cells = []
            for j, value in enumerate(row):
                # Formatting cells: align in center
                row_cells.append({
                    "userEnteredValue": {"stringValue": value},
                    "userEnteredFormat": {"horizontalAlignment": "CENTER"}
                })
            batch_requests.append({
                "updateCells": {
                    "range": {
                        "sheetId": 0,
                        "startRowIndex": i,
                        "endRowIndex": i + 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": len(row)
                    },
                    "rows": [{"values": row_cells}],
                    "fields": "userEnteredValue,userEnteredFormat"
                }
            })

        # Split batch_requests into chunks of 1000 requests each (REQUEST LIMIT 1000)
        chunked_requests = [batch_requests[i:i + 1000] for i in range(0, len(batch_requests), 1000)]

        # Run requests to Google Sheets API
        for index, chunk in enumerate(chunked_requests):
            # Timeout
            time.sleep(timeout)

            logging.info(f"Processing chunk {index + 1}/{len(chunked_requests)}")
            batch_update_body = {"requests": chunk}

            # Sending a batch of table update requests
            response = service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=batch_update_body).execute()
            logging.info(f"Chunk {index + 1} processed")


def main() -> None:
    # Auth
    client, service = GoogleSheetsApiAuth.get_google_services()

    # Open Google Sheet by Sheet id
    spreadsheet = client.open_by_key(sheet_id)
    spreadsheet = spreadsheet.sheet1

    # GET cells
    data, ref_column, type_column = GoogleSheetsApiAuth.get_sheet(spreadsheet)

    # Check if Ref row is sorted
    if ref_column != sorted(ref_column):
        sorted_data = CellSorter.sort_data(data, ref_column)
        SheetUpdater.update_sheet(service, sheet_id, sorted_data)
        logging.info("Created a new sheet with sorted data.")
    else:
        logging.info("Data is already sorted.")

    # Color the cells
    CellFormatter.color_by_type(service, ref_column, type_column, sheet_id)
    logging.info("Data is already sorted.")


if __name__ == "__main__":
    main()
