from app.csv_importer.importer import AbstractImporter
from datetime import datetime

class MonzoImporter(AbstractImporter):
    def get_date(self, row):
        return datetime.strptime(row['Date'], '%d/%m/%Y')

    def get_time(self, row):
        return row['Time']

    def get_title(self, row):
        return row['Name']

    def get_currency(self, row):
        return row['Currency']

    def get_amount(self, row):
        return row['Amount']

    def get_category(self, row):
        return row['Category']

    def get_notes(self, row):
        return row['Notes and #tags']