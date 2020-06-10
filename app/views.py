# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import template
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from app.forms import AccountCreateForm, AccountUpdateForm
from app.models import Account

@login_required
def index(request):
    return render(request, "index.html")

@login_required
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))


class AccountCreateView(LoginRequiredMixin, CreateView):
    form_class = AccountCreateForm
    template_name = 'account_create_update.html'
    success_url = reverse_lazy('accounts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label_card_title'] = "Create New Account"
        context['label_submit_button'] = "Create"
        return context


class AccountListView(LoginRequiredMixin, ListView):
    template_name = 'accounts.html'
    model = Account

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountUpdateForm
    template_name = 'account_create_update.html'
    success_url = reverse_lazy('accounts')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(AccountUpdateView, self).get_context_data(**kwargs)
        context['label_card_title'] = "Update Account"
        context['label_submit_button'] = "Update"
        return context


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    success_url = reverse_lazy('accounts')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
