import logging

from config import GoogleSheetsApiAuth, sheet_id
from fold import FoldProcess
from insert_data import CopyToNewPage
from sorting import CellSorter


def main() -> None:
    # Auth
    client, service = GoogleSheetsApiAuth.get_google_services()

    # Open Google Sheet by Sheet id
    spreadsheet = client.open_by_key(sheet_id).sheet1
    data, ref_column, type_column = GoogleSheetsApiAuth.get_sheet(spreadsheet)

    # Sorting
    CellSorter.sort_data(spreadsheet)

    # Process to Fold lines
    edited_rows = FoldProcess.process_table(data)

    # Insert fold data into Result page
    CopyToNewPage.copy_to_result_sheet(service, sheet_id, spreadsheet, edited_rows)


if __name__ == "__main__":
    main()
