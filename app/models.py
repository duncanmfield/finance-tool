# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=128)
    type = models.CharField(max_length=128)
    is_internal = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now=True)
    balance = models.IntegerField()

    def __str__(self):
        return self.name
