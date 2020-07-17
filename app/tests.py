# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.models import User
from django.test import TestCase

from app.models import Account
from app.templatetags import currency_formatting


class AccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

        self.personal = Account.objects.create(user_id=self.user.id, name='A')

    def test_account_model(self):
        # Arrange
        queryset = Account.objects.all()

        # Act

        # Assert
        self.assertEqual(self.personal.name, 'A')
        self.assertIsNotNone(queryset.first().balance)
        self.assertTrue(queryset.first().type in Account.TYPE_CHOICES[0][1])


class CurrencyFormattingTests(TestCase):
    def setUp(self):
        pass

    def test_currency_codes_are_3_characters(self):
        # Arrange
        codes = currency_formatting.CURRENCY_SYMBOLS.keys()

        # Act

        # Assert
        self.assertGreater(len(codes), 0)

        for code in codes:
            self.assertIs(len(code), 3, "Currency code '{}' should have a length of 3".format(code))

    def test_currency_symbols_are_1_character(self):
        # Arrange
        symbols = currency_formatting.CURRENCY_SYMBOLS.values()

        # Act

        # Assert
        self.assertGreater(len(symbols), 0)

        for symbol in symbols:
            self.assertIs(len(symbol), 1, "Currency symbol '{}' should have a length of 1".format(symbol))