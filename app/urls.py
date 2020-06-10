# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf.urls import url
from django.urls import path, re_path
from app import views

urlpatterns = [
    path('accounts.html', views.AccountListView.as_view(), name='accounts'),
    path('account_create.html', views.AccountCreateView.as_view(), name='account_create'),
    url(r'^account_delete/(?P<pk>\d+)/$', views.AccountDeleteView.as_view(), name='delete_view'),

    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
]
