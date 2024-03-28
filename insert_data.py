import gspread
import logging

from config import GoogleSheetsApiAuth
from formatting import CellFormatter


class CopyToNewPage:

    @staticmethod
    def create_new_sheet(parent_spreadsheet):
        """ Create a new Google Sheet """

        try:
            # Check if the "Result" worksheet exists
            result_sheet = parent_spreadsheet.worksheet("Result")
            logging.info("Worksheet Result already exists")

        except gspread.exceptions.WorksheetNotFound:
            # If the worksheet doesn't exist, create a new one
            result_sheet = parent_spreadsheet.add_worksheet(title="Result", rows="100", cols="20")
            logging.info("Created a new worksheet Result")

        return result_sheet

    @staticmethod
    def copy_to_result_sheet(service, sheet_id: str, spreadsheet, data: list[list[str]]):
        """ Insert fold data into Result sheet """

        # Get the parent spreadsheet from the worksheet object
        parent_spreadsheet = spreadsheet.spreadsheet

        # Create new table
        result_sheet = CopyToNewPage.create_new_sheet(parent_spreadsheet)

        # Clear existing data in the "Result" worksheet
        result_sheet.clear()

        # Append the new data to the "Result" worksheet
        result_sheet.update('A1', data)
        logging.info("Updated 'Result' worksheet with new data.")

        data, ref_column, type_column = GoogleSheetsApiAuth.get_sheet(result_sheet)

        # (Formatting) Color the cells
        CellFormatter.color_first_row(service, result_sheet)
        CellFormatter.color_by_type(service, ref_column, type_column, result_sheet)
        CellFormatter.format_center_data(service, sheet_id, result_sheet)
