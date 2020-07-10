# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf import settings
from django.db import models

# Create your models here.
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
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.name
