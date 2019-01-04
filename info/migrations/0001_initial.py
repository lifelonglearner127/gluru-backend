# Generated by Django 2.1.3 on 2019-01-04 07:47

import django.contrib.postgres.fields
import django.contrib.postgres.fields.citext
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GluuProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(max_length=20, unique=True)),
                ('version', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=None)),
                ('os', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='HighIssueTypeManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='LowIssueTypeManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=20)),
                ('model_name', models.CharField(max_length=20)),
                ('actions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=None)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TicketCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Ticket Categories',
            },
        ),
        migrations.CreateModel(
            name='TicketIssueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(max_length=30, unique=True)),
                ('priority', models.CharField(choices=[('high', 'High'), ('low', 'Low')], default='low', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TicketStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Ticket Status',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(max_length=20, unique=True)),
                ('is_company_associated', models.BooleanField(default=False)),
                ('permissions', models.ManyToManyField(to='info.Permission')),
            ],
        ),
    ]
