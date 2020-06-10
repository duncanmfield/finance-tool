# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms

from app.models import Account

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
