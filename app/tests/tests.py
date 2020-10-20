# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""
import os
from datetime import datetime

from django.contrib.auth.models import User
from django.template import Context
from django.test import TestCase
from django.urls import reverse

from app.csv_importer.monzo_importer import MonzoImporter
from app.forms import AccountCreateForm, AccountUpdateForm, UserSettingsUpdateForm
from app.models import Account, Transaction
from app.templatetags import currency_formatting


class AccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

        self.personal = Account.objects.create(user_id=self.user.id, name='A')

    def test_str_is_name(self):
        self.assertEqual(str(self.personal), self.personal.name)

    def test_account_model(self):
        # Arrange
        queryset = Account.objects.all()

        # Act

        # Assert
        self.assertEqual(self.personal.name, 'A')
        self.assertIsNotNone(queryset.first().balance)
        self.assertTrue(queryset.first().type in Account.TYPE_CHOICES[0])


class AccountCreateFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

    def test_default_create_form_is_invalid(self):
        # Arrange
        form = AccountCreateForm()

        # Act

        # Assert
        self.assertFalse(form.is_valid())

    def test_create_form_is_valid(self):
        # Arrange
        data = {'name': 'Foo', 'type': Account.TYPE_CHOICES[0][0], 'initial_balance': 0}
        form = AccountCreateForm(data=data)

        # Act

        # Assert
        self.assertTrue(form.is_valid())


class AccountUpdateFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

    def test_default_update_form_is_invalid(self):
        # Arrange
        form = AccountUpdateForm()

        # Act

        # Assert
        self.assertFalse(form.is_valid())

    def test_update_form_is_valid(self):
        # Arrange
        data = {'name': 'Foo', 'type': Account.TYPE_CHOICES[0][0], 'initial_balance': 0}
        form = AccountUpdateForm(data=data)

        # Act

        # Assert
        self.assertTrue(form.is_valid())


class UserSettingsUpdateFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

    def test_default_update_form_is_invalid(self):
        # Arrange
        form = UserSettingsUpdateForm()

        # Act

        # Assert
        self.assertFalse(form.is_valid())

    def test_update_form_is_valid(self):
        # Arrange
        data = {'currency': list(currency_formatting.CURRENCY_SYMBOLS)[0],
                'number_format': list(currency_formatting.NUMBER_FORMATTING_OPTIONS)[0]}
        form = UserSettingsUpdateForm(data=data)

        # Act

        # Assert
        self.assertTrue(form.is_valid())


class CurrencyFormattingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

    def test_currency_codes_are_3_characters(self):
        # Arrange
        codes = currency_formatting.CURRENCY_SYMBOLS.keys()

        # Act

        # Assert
        self.assertGreater(len(codes), 0)

        for code in codes:
            self.assertEqual(len(code), 3, msg="Currency code '{}' should have a length of 3".format(code))

    def test_currency_symbols_are_1_character(self):
        # Arrange
        symbols = currency_formatting.CURRENCY_SYMBOLS.values()

        # Act

        # Assert
        self.assertGreater(len(symbols), 0)

        for symbol in symbols:
            self.assertEqual(len(symbol), 1, msg="Currency symbol '{}' should have a length of 1".format(symbol))

    def test_default_formatting_is_valid(self):
        # Arrange
        initial_value = 1234.56

        # Act
        formatted_value = currency_formatting.as_currency_with_user(self.user, initial_value)

        # Assert
        self.assertTrue("1" in formatted_value)
        self.assertTrue("234" in formatted_value)
        self.assertTrue("56" in formatted_value)

    def test_invalid_as_currency_tag_retains_digits(self):
        # Arrange
        self.user.settings.currency = 'InvalidType'
        initial_value = 1234.56
        context = Context({"user": self.user})

        # Act
        formatted_value = currency_formatting.as_currency(context, initial_value)

        # Assert
        self.assertTrue("1" in formatted_value)
        self.assertTrue("234" in formatted_value)
        self.assertTrue("56" in formatted_value)

    def test_as_currency_tag_retains_digits(self):
        # Arrange
        initial_value = 1234.56
        context = Context({"user": self.user})

        # Act
        formatted_value = currency_formatting.as_currency(context, initial_value)

        # Assert
        self.assertTrue("1" in formatted_value)
        self.assertTrue("234" in formatted_value)
        self.assertTrue("56" in formatted_value)

    def test_currency_symbol_tag_adds_symbol(self):
        # Arrange
        context = Context({"user": self.user})

        # Act
        symbol = currency_formatting.currency_symbol(context)

        # Assert
        self.assertEqual(len(symbol), 1)


class ViewTests(TestCase):
    def test_logged_out_redirects_to_valid_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertGreater(len(response.url), 0)

        redirect_page_response = self.client.get(response.url)
        self.assertEqual(redirect_page_response.status_code, 200)


class ImporterTests(TestCase):
    def test_monzo_importer(self):
        test_file_path = os.path.join(os.path.dirname(__file__), 'resources', 'valid_monzo_import.txt')
        importer = MonzoImporter(open(test_file_path).read())
        transactions, invalid_rows = importer.read()

        expected_1 = Transaction(title="JOHN SMITH",
                                 notes="MONZO TOPUP",
                                 date=datetime.strptime("13/08/2019", "%d/%m/%Y").date(),
                                 time=datetime.strptime("11:46:05", "%H:%M:%S").time(),
                                 amount=100.00)

        expected_2 = Transaction(title="Sports Centre",
                                 notes="",
                                 date=datetime.strptime("15/08/2019", "%d/%m/%Y").date(),
                                 time=datetime.strptime("14:48:53", "%H:%M:%S").time(),
                                 amount=-7.50)

        self.assertTransactionEqual(expected_1, transactions[0])
        self.assertTransactionEqual(expected_2, transactions[1])

    def assertTransactionEqual(self, expected, actual):
        self.assertEqual(expected.title, actual.title)
        self.assertEqual(expected.notes, actual.notes)
        self.assertEqual(expected.date, actual.date)
        self.assertEqual(expected.time, actual.time)
        self.assertEqual(expected.amount, actual.amount)
