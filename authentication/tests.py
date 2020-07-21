# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from authentication.forms import LoginForm, SignUpForm


class LoginViewTests(TestCase):
    def test_login_form_shown_if_logged_out(self):
        # Arrange

        # Act
        response = self.client.get(reverse('login'))

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(type(response.context['form']), LoginForm)

    def test_login_view_redirects_if_logged_in(self):
        # Arrange
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

        # Act
        response = self.client.get(reverse('login'))

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_login_view_denies_blank_request(self):
        # Arrange

        # Act
        response = self.client.post(reverse('login'))

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(type(response.context['form']), LoginForm)

    def test_login_view_denies_wrong_password(self):
        # Arrange
        self.user = User.objects.create_user(username='test', password='12345')

        # Act
        response = self.client.post(reverse('login'), data={'username': 'test', 'password': '1234'})

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(type(response.context['form']), LoginForm)

    def test_login_view_redirects_valid_login(self):
        # Arrange
        self.user = User.objects.create_user(username='test', password='12345')

        # Act
        response = self.client.post(reverse('login'), data={'username': 'test', 'password': '12345'})

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))


class RegisterViewTests(TestCase):
    def test_register_form_shown_if_logged_out(self):
        # Arrange

        # Act
        response = self.client.get(reverse('register'))

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(type(response.context['form']), SignUpForm)

    def test_register_view_redirects_if_logged_in(self):
        # Arrange
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

        # Act
        response = self.client.get(reverse('register'))

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_register_view_denies_blank_request(self):
        # Arrange

        # Act
        response = self.client.post(reverse('register'))

        # Assert
        self.assertFalse(response.context['success'])

    def test_register_view_denies_duplicate_user(self):
        # Arrange
        username = 'test'
        self.user = User.objects.create_user(username=username, password='12345')
        duplicate_user_data = {'username': username,
                      'email': 'test@example.com',
                      'password1': 'VaLiD_P4Ss',
                      'password2': 'VaLiD_P4Ss'}

        # Act
        response = self.client.post(reverse('register'), duplicate_user_data)

        # Assert
        self.assertFalse(response.context['success'])

    def test_register_view_accepts_valid_details(self):
        # Arrange
        valid_data = {'username': 'test',
                      'email': 'test@example.com',
                      'password1': 'VaLiD_P4Ss',
                      'password2': 'VaLiD_P4Ss'}

        # Act
        response = self.client.post(reverse('register'), valid_data)

        # Assert
        self.assertTrue(response.context['success'])

    def test_register_view_denies_different_passwords(self):
        # Arrange
        valid_data = {'username': 'test',
                      'email': 'test@example.com',
                      'password1': 'VaLiD_P4Ss',
                      'password2': 'InVaLiD_P4Ss'}

        # Act
        response = self.client.post(reverse('register'), valid_data)

        # Assert
        self.assertFalse(response.context['success'])