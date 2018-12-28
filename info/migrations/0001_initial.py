# Generated by Django 2.1.3 on 2018-12-27 16:22

import django.contrib.postgres.fields
import django.contrib.postgres.fields.citext
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GluuOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Gluu OS',
            },
        ),
        migrations.CreateModel(
            name='GluuProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(max_length=20, unique=True)),
                ('version', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.citext.CICharField(max_length=20, unique=True), size=None)),
                ('os', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.citext.CICharField(max_length=20, unique=True), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='GluuServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(max_length=20, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
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
                ('actions', models.TextField()),
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
                ('permissions', models.ManyToManyField(to='info.Permission')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='permission',
            unique_together={('app_name', 'model_name', 'actions')},
        ),
    ]
