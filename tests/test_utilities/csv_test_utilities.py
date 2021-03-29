import csv


class CsvTestChecker:
    """
    Utilities to help in checking that CSV files created by the app are correct, to aid testing.
    """
    def __init__(self, csv_path):
        self.path = csv_path

    def check(self, row, column, value):
        with open(self.path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row_num, record in enumerate(reader):
                if row_num == row+1:  # Add one to allow for header
                    if record[column] == value:
                        return True
                    else:
                        return False
