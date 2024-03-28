import gspread

# Call the function to color the first row
blue_color = {"red": 74, "green": 134, "blue": 232}

#  Color for painting cells
colors = {
    "0": {"red": 201, "green": 218, "blue": 248},
    "2": {"red": 183, "green": 225, "blue": 205},
    "3": {"red": 87, "green": 187, "blue": 138},
    "13": {"red": 217, "green": 234, "blue": 211},
    "23": {"red": 234, "green": 209, "blue": 220},
}


class CellFormatter:
    """ Format cells bg-color """

    @staticmethod
    def rgb_to_color(rgb: dict[str, int]) -> dict[str, float]:
        """ Converts RGB values to color format accepted by Google Sheets API """

        r = rgb.get("red") / 255
        g = rgb.get("green") / 255
        b = rgb.get("blue") / 255
        return {"red": r, "green": g, "blue": b}

    @staticmethod
    def color_first_row(service, result_sheet: gspread.Worksheet) -> None:
        """ Color the entire first row of the worksheet with the specified color """

        batch_request = {
            "repeatCell": {
                "range": {
                    "sheetId": result_sheet.id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": result_sheet.row_count
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": CellFormatter.rgb_to_color(blue_color),
                        "horizontalAlignment": "CENTER",
                        "textFormat": {
                            "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
                            "fontSize": 11,
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
            }
        }

        # Send the request to update the color of the first row
        service.spreadsheets().batchUpdate(
            spreadsheetId=result_sheet.spreadsheet.id,
            body={"requests": [batch_request]}
        ).execute()

    @staticmethod
    def color_by_type(service, ref_column: list[str], type_column: list[str], result_sheet: gspread.Worksheet) -> None:
        """ Paint the cells background by Type """

        batch_requests = []

        # GET "Result" page ID
        sheet_id = result_sheet.id
        print()

        # Iterate по ref_column | type_column
        for ref, type_value in zip(ref_column, type_column):
            type_value_str = str(type_value)

            # Check if a color exist for this Type
            if type_value_str in colors:

                # GET color correspond to Type
                color = CellFormatter.rgb_to_color(colors[type_value_str])

                # GET index line, which need to color
                ref_rows_to_color = [i for i, ref_value in enumerate(ref_column, start=1) if ref_value == ref]
                for row in ref_rows_to_color:
                    row_index = row + 1
                    request = {
                        "repeatCell": {
                            "range": {
                                "sheetId": sheet_id,
                                "startRowIndex": row_index - 1,
                                "endRowIndex": row_index,
                                "startColumnIndex": 0,
                                "endColumnIndex": 1
                            },
                            "cell": {
                                "userEnteredFormat": {
                                    "backgroundColor": color,
                                    "horizontalAlignment": "CENTER",
                                }
                            },
                            "fields": "userEnteredFormat(backgroundColor, horizontalAlignment)"
                        }
                    }
                    batch_requests.append(request)

        # Sent all requests with updated colors in one batch
        (service.spreadsheets().batchUpdate(
            spreadsheetId=result_sheet.spreadsheet.id,
            body={"requests": batch_requests}
        ).execute())

    @staticmethod
    def format_center_data(service, sheet_id: str, sheet):
        """ Format the cells value in center """
        result_sheet_id = sheet._properties['sheetId']  # Get the sheet ID
        requests = [{
            "repeatCell": {
                "range": {"sheetId": result_sheet_id},
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat.horizontalAlignment"
            }
        }]

        # Sent all requests with updated colors in one batch
        service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body={"requests": requests}).execute()
