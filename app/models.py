# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.templatetags.currency_formatting import CURRENCY_SYMBOLS, NUMBER_FORMATTING_OPTIONS
from datetime import date


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    currency_choices = [(code, "{} ({})".format(code, CURRENCY_SYMBOLS.get(code))) for code in CURRENCY_SYMBOLS.keys()]
    currency = models.CharField(max_length=3, choices=currency_choices, default=currency_choices[0][0])

    number_formatting_choices = [(option, NUMBER_FORMATTING_OPTIONS.get(option).format(1234.56)) for option in NUMBER_FORMATTING_OPTIONS.keys()]
    number_format = models.CharField(max_length=32, choices=number_formatting_choices, default=number_formatting_choices[0][0])

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Settings.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.settings.save()


class Account(models.Model):
    BANK_ACCOUNT = 0
    SAVINGS_ACCOUNT = 1
    PENSION = 2
    CASH = 3
    ASSET = 4
    LIABILITY = 5
    TYPE_CHOICES = (
        (BANK_ACCOUNT, 'Bank Account'),
        (SAVINGS_ACCOUNT, 'Savings Account'),
        (PENSION, 'Pension'),
        (CASH, 'Cash'),
        (ASSET, 'Asset'),
        (LIABILITY, 'Liability'),
    )

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    type = models.IntegerField(choices=TYPE_CHOICES)
    is_internal = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0) # Replace with equivalent of @property def balance(self, date): Transactions.objects.filter(account=self, date__lte=date).aggregate(models.Sum('amount'))['amount__sum']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64)
    last_modified = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    class Meta:
        ordering = ['-date', 'title']

    date = models.DateField(default=date.today)
    title = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    source = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='source')
    destination = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='destination')
    notes = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, blank=True, null=True)
