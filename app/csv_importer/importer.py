from csv import reader
from abc import ABC, abstractmethod
from io import StringIO
from django.core.exceptions import ValidationError
from app.models import Transaction


class AbstractImporter(ABC):
    def __init__(self, file):
        self.file_contents = file
        self.valid_transactions = []
        self.invalid_rows = []
        pass

    def process_row(self, row):
        transaction = Transaction()

        try:
            transaction.id = self.get_transaction_id(row)
            transaction.date = self.get_date(row).strftime('%Y-%m-%d')
            transaction.time = self.get_time(row)
            transaction.title = self.get_title(row)
            transaction.amount = '{:.2f}'.format(float(str(self.get_amount(row))))
            transaction.notes = self.get_notes(row)
        except:
            self.invalid_rows.append(row)
        else:
            self.validate_transaction(transaction, row)

    def validate_transaction(self, transaction, row):
        try:
            transaction.full_clean(exclude=['user', 'source'])
        except ValidationError:
            self.invalid_rows.append(row)
        else:
            self.valid_transactions.append(transaction)

    def read(self):
        # TODO : Have the user pick an account to import the CSV in to
        csv_data = reader(StringIO(self.file_contents), delimiter=',')
        headers = next(csv_data)

        # Process each row of the CSV
        for raw_row_data in csv_data:
            row = dict(zip(headers, raw_row_data))
            self.process_row(row)

        return self.valid_transactions, self.invalid_rows

    @abstractmethod
    def get_transaction_id(self, row):
        pass

    @abstractmethod
    def get_date(self, row):
        """Should return instance of datetime.datetime"""
        pass

    @abstractmethod
    def get_time(self, row):
        pass

    @abstractmethod
    def get_title(self, row):
        pass

    @abstractmethod
    def get_amount(self, row):
        pass

    @abstractmethod
    def get_category(self, row):
        pass

    @abstractmethod
    def get_notes(self, row):
        pass