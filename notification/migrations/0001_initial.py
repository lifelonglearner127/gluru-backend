# Generated by Django 2.1.3 on 2018-12-05 15:31

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailRecipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResponseTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('support_plan', models.CharField(max_length=20)),
                ('issue_type', models.CharField(max_length=20)),
                ('response_time', models.IntegerField()),
            ],
            options={
                'ordering': ['support_plan', 'issue_type'],
            },
        ),
        migrations.CreateModel(
            name='SMSContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='responsetime',
            unique_together={('support_plan', 'issue_type')},
        ),
    ]
