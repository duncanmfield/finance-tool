# Generated by Django 2.2.13 on 2020-07-16 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='currency',
            field=models.CharField(choices=[('GBP', 'GBP'), ('USD', 'USD'), ('EUR', 'EUR')], default='GBP', max_length=3),
        ),
    ]