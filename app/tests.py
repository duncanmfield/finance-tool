# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.models import User
from django.test import TestCase

from app.models import Account


class AccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

        self.personal = Account.objects.create(user_id=self.user.id, name='A')
        self.foreign = Account.objects.create(user_id=self.user.id, name='B', type=Account.TYPE_CHOICES[0][1])

    def test_account_model(self):
        queryset = Account.objects.all()
        self.assertEqual(queryset.count(), 2)
        self.assertEqual(queryset.first(), self.personal)
