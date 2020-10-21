# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.core.exceptions import ValidationError

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
        self.fields['initial_balance'].widget.attrs = {
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
        fields = ('name', 'type', 'initial_balance', 'is_internal')


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
        self.fields['initial_balance'].widget.attrs = {
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
        fields = ('name', 'type', 'initial_balance', 'is_internal')


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


def file_size(value):  # add this to some file where you can import it from
    limit_mib = 5
    limit = limit_mib * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed ' + str(limit_mib) + ' MiB.')


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a CSV file', validators=[file_size])
    account = forms.ModelChoiceField(queryset=None)

    def __init__(self, accounts=None, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs = {
            'placeholder': 'CSV File',
            'class': 'file-upload-default'
        }
        self.fields['account'].widget.attrs = {
            'class': 'form-control'
        }

        self.fields['account'].queryset = accounts