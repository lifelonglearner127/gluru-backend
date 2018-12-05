# Generated by Django 2.1.3 on 2018-12-05 17:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('op_host', models.CharField(blank=True, max_length=255, verbose_name='op host')),
                ('oxd_host', models.CharField(blank=True, max_length=255, verbose_name='oxd host')),
                ('oxd_id', models.CharField(blank=True, max_length=255, verbose_name='oxd id')),
                ('authorization_redirect_uri', models.URLField(blank=True, verbose_name='authorization redirect uri')),
                ('post_logout_redirect_uri', models.URLField(blank=True, verbose_name='post logout redirect uri')),
                ('client_name', models.CharField(blank=True, max_length=255, verbose_name='client name')),
                ('client_id', models.CharField(blank=True, max_length=255, verbose_name='client id')),
                ('client_secret', models.CharField(blank=True, max_length=255, verbose_name='client secret')),
                ('scope', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, size=None)),
                ('grant_types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, size=None)),
                ('protection_access_token', models.CharField(blank=True, max_length=255, verbose_name='protection access token')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='last login')),
            ],
        ),
        migrations.CreateModel(
            name='LoginState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.TextField(blank=True, verbose_name='state')),
                ('nonce', models.TextField(blank=True, verbose_name='state')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
            ],
        ),
        migrations.CreateModel(
            name='LogoutState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.TextField(blank=True, verbose_name='state')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
            ],
        ),
    ]
