# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf.urls import url
from django.urls import path, re_path
from app import views

urlpatterns = [
    path('accounts/', views.AccountListView.as_view(), name='accounts'),
    path('account_create/', views.AccountCreateView.as_view(), name='account_create'),
    url(r'^account_update/(?P<pk>\d+)/$', views.AccountUpdateView.as_view(), name='account_update'),
    url(r'^account_delete/(?P<pk>\d+)/$', views.AccountDeleteView.as_view(), name='account_delete'),
    path('account_values_chart/', views.account_values_chart, name='account_values_chart'),

    path('user_settings/', views.UserSettingsUpdateView.as_view(), name='user_settings'),

    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
]
