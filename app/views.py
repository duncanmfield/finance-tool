# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django import template
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from app.csv_importer.monzo_importer import MonzoImporter
from app.forms import AccountCreateForm, AccountUpdateForm, UserSettingsUpdateForm, UploadFileForm
from app.models import Account, Settings, Transaction
from app.templatetags.currency_formatting import as_currency_with_user


@login_required
def index(request):
    queryset = Account.objects.filter(user=request.user, is_internal=True)

    net_worth = 0
    for account in queryset:
        net_worth = net_worth + account.balance

    context = {"net_worth": net_worth}

    return render(request=request, template_name="index.html", context=context)

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


def account_values_chart(request):
    queryset = Account.objects.filter(user=request.user, is_internal=True)

    labels = []
    data = []
    total = 0

    for account in queryset:
        labels.append(account.name)
        data.append(account.balance)
        total += account.balance

    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'centerText': as_currency_with_user(request.user, total),
        'centerSubText': 'Total',
        'colorPalette': 'cb-Greens',
    })

class UserSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = Settings
    form_class = UserSettingsUpdateForm
    template_name = 'user_settings_update.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().first()

    def get_context_data(self, **kwargs):
        context = super(UserSettingsUpdateView, self).get_context_data(**kwargs)
        return context


def get_paginate_range(current_page, total_pages):
    paginate_either_side = 5
    max_paginate_size = paginate_either_side * 2 + 1

    start_page = max(1, current_page - paginate_either_side)
    end_page = min(total_pages + 1, start_page + max_paginate_size)

    if end_page - start_page < max_paginate_size:
        start_page = max(1, end_page - max_paginate_size)

    return range(start_page, end_page)


class TransactionListView(LoginRequiredMixin, ListView):
    template_name = 'transactions.html'
    paginate_by = 30
    model = Transaction

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        context['paginate_range'] = get_paginate_range(context['page_obj'].number,
                                                       context['page_obj'].paginator.num_pages)
        return context

class TransactionInListView(TransactionListView):
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, amount__gt=0)

class TransactionOutListView(TransactionListView):
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, amount__lte=0)


@login_required
def import_transactions(request):
    success_url = reverse_lazy('accounts')
    accounts = Account.objects.filter(user=request.user, is_internal=True)

    if request.method == 'POST':
        form = UploadFileForm(accounts, request.POST, request.FILES)
        if form.is_valid():
            importer = MonzoImporter(request.FILES['file'].read().decode('utf-8'))
            transactions, invalid_rows = importer.read()

            if len(transactions) > 0:
                for transaction in transactions:
                    transaction.source = form.cleaned_data['account']
                    transaction.user = request.user
                    transaction.save()

                return HttpResponseRedirect(success_url)
            else:
                form.add_error('file', 'File has no new transactions or is not a supported CSV type')
    else:
        form = UploadFileForm(accounts)

    return render(request=request, template_name='import_transactions.html', context={'form': form})