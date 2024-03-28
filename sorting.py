import gspread
import logging
from config import GoogleSheetsApiAuth


class CellSorter:

    @staticmethod
    def compare_ref_column(ref_column: list[str]):
        """ Compare original and sorted ref_column """

        sorted_ref_column = sorted(ref_column)
        for original, sorted_item in zip(ref_column, sorted_ref_column):
            if original != sorted_item:
                logging.error(f"[ERROR] {original}\t{sorted_item}")

    @staticmethod
    def sort_data(spreadsheet):
        """ Sort table by (ref_column) """

        data, ref_column, type_column = GoogleSheetsApiAuth.get_sheet(spreadsheet)

        if ref_column != sorted(ref_column):
            """ Check if ref_column is sorted in ascending order """

            # Compare original and sorted ref_column
            CellSorter.compare_ref_column(ref_column)

            # Ref Row
            ref_column = 1

            # Calculating the number of cells in a table
            total_rows = spreadsheet.row_count
            total_cols = spreadsheet.col_count

            # Find the A1 notation of the last cell
            last_cell_a1 = gspread.utils.rowcol_to_a1(total_rows, total_cols)

            # Sort from A2 to the last cell
            spreadsheet.sort((ref_column, 'asc'), range=f'A2:{last_cell_a1}')

            logging.info("Data is sorted successfully!")
        else:
            logging.info("Data is already sorted!")
