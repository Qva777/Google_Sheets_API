class FoldProcess:
    @staticmethod
    def process_table(data: list[list[str]]) -> list[list[str]]:
        """ Process of iteration table data  """

        edited_rows = []
        merged_indices = set()

        for i, row in enumerate(data):
            type_column = row[9]
            if type_column == "23" or type_column == "2":
                current_index = i
                edited_rows.append(row)

                # Range of Type 13 in 23 | 2
                merged_indices, merged_result, num_remaining_13 = FoldProcess.process_from_current_index(data,
                                                                                                         current_index)

                merged_indices.update(merged_indices)
                edited_rows.extend(merged_result)

                if len(merged_result) == 1:
                    # Delete a string like 13 if it was combined with 23 | 2
                    del edited_rows[-1]

            elif type_column != "23" and type_column != "13":
                #  Add strings with Type 3 | 0 | other
                edited_rows.append(row)

        return edited_rows

    @staticmethod
    def process_from_current_index(input_table: list[list[str]], start_index: int) \
            -> tuple[set[int], list[list[str]], int]:
        """ Process rows in the input_table starting from the given start_index """

        merged_rows = []
        merged_indices = set()

        for i in range(start_index + 1, len(input_table)):
            type_column = input_table[i][9]
            if type_column != "13":
                break
            else:
                merged_rows.append(input_table[i])
                merged_indices.add(i)

        # Merge rows with duplicate value
        merged_result = CellMargeUpdate.merge_duplicate_rows(merged_rows)

        if len(merged_result) == 1:
            # Transfer values from type 13 to parent list of type 23 | 2
            for row in merged_result:
                for j, val in enumerate(row):
                    if input_table[start_index][j] == '' and val != '':
                        input_table[start_index][j] = val

        if len(merged_result) == 1:
            # Remove lines like 13 from the source list if 23 | 2 is followed by only one line 13
            for index in sorted(merged_indices, reverse=True):
                del input_table[index]

        # See how many lines like 13 are left after lines like 23 | 2
        num_remaining_13 = sum(1 for row in input_table[start_index + 1:] if row[9] == '13')

        return merged_indices, merged_result, num_remaining_13


class CellMargeUpdate:
    @staticmethod
    def merge_duplicate_rows(rows: list[list[str]]) -> list[list[str]]:
        """ Merge duplicate rows based on specific columns """

        merged_rows = []
        seen = {}

        for row in rows:
            key = tuple(row[10:12] + row[14:16])

            if key in seen:
                index = seen[key]
                merged_rows[index] = CellMargeUpdate.update_row(merged_rows[index], row)
            else:
                seen[key] = len(merged_rows)
                merged_rows.append(row)

        return merged_rows

    @staticmethod
    def update_row(existing_row, new_row):
        """ Transfer (Unit | Pack | Color Ref | Color) from child to parent line """

        updated_row = existing_row[:]

        updated_row[6] = " ".join(set(existing_row[6].split() + new_row[6].split()))
        updated_row[7] = " ".join(set(existing_row[7].split() + new_row[7].split()))

        updated_row[12] = " ".join(set(existing_row[12].split() + new_row[12].split()))
        updated_row[13] = " ".join(set(existing_row[13].split() + new_row[13].split()))

        return updated_row
