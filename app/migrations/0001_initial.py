# Generated by Django 2.2.13 on 2020-06-08 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=128)),
                ('is_internal', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('balance', models.IntegerField()),
            ],
        ),
    ]
