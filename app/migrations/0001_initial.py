# Generated by Django 2.2.13 on 2020-07-16 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('GBP', 'GBP'), ('USD', 'USD'), ('EUR', 'EUR')], default=('GBP', 'GBP'), max_length=3)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(choices=[('Bank Account', 'Bank Account'), ('Savings Account', 'Savings Account'), ('Pension', 'Pension'), ('Cash', 'Cash'), ('Asset', 'Asset'), ('Liability', 'Liability')], default='Bank Account', max_length=32)),
                ('is_internal', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=14)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
