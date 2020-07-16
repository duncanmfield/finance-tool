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
    TYPE_CHOICES = (
        ("Bank Account", 'Bank Account'),
        ("Savings Account", 'Savings Account'),
        ("Pension", 'Pension'),
        ("Cash", 'Cash'),
        ("Asset", 'Asset'),
        ("Liability", 'Liability'),
    )

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=32, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][1])
    is_internal = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return self.name
