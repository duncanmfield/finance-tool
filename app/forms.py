# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from app.models import Account, Settings


class AccountCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'placeholder': 'Name',
            'class': 'form-control'
        }
        self.fields['type'].widget.attrs = {
            'placeholder': 'Account Type',
            'class': 'form-control'
        }
        self.fields['balance'].widget.attrs = {
            'placeholder': 'Initial Balance',
            'class': 'form-control'
        }
        self.fields['is_internal'].widget.attrs = {
            'class': 'form-check-input'
        }
        self.fields['is_internal'].label = 'Is Internal'
        self.fields['is_internal'].label_suffix = ''

    class Meta:
        model = Account
        fields = ('name', 'type', 'balance', 'is_internal')

class AccountUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'placeholder': 'Name',
            'class': 'form-control'
        }
        self.fields['type'].widget.attrs = {
            'placeholder': 'Account Type',
            'class': 'form-control'
        }
        self.fields['balance'].widget.attrs = {
            'placeholder': 'Initial Balance',
            'class': 'form-control'
        }
        self.fields['is_internal'].widget.attrs = {
            'class': 'form-check-input'
        }
        self.fields['is_internal'].label = 'Internal'
        self.fields['is_internal'].label_suffix = ''

    class Meta:
        model = Account
        fields = ('name', 'type', 'balance', 'is_internal')

class UserSettingsUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserSettingsUpdateForm, self).__init__(*args, **kwargs)
        self.fields['currency'].widget.attrs = {
            'placeholder': 'Currency',
            'class': 'form-control'
        }
        self.fields['number_format'].widget.attrs = {
            'placeholder': 'Number Format',
            'class': 'form-control'
        }

    class Meta:
        model = Settings
        fields = ('currency', 'number_format')
