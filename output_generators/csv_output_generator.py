import csv


class CsvOutputGenerator:
    @staticmethod
    def create_csv_file(data_table, output_path):
        # Use first record to extract field names.
        # ToDo: Find cleaner way of passing field names.  Shouldn't need to derive from a data record.
        field_names = [key for key in data_table[0]]

        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            for row in data_table:
                writer.writerow(row)
