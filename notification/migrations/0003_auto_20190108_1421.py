# Generated by Django 2.1.3 on 2019-01-08 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_notificationsetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationsetting',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notification_setting', to=settings.AUTH_USER_MODEL),
        ),
    ]
