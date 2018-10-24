# Generated by Django 2.1.2 on 2018-10-24 02:05

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
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('link_url', models.URLField(blank=True, max_length=255, verbose_name='Link URL')),
                ('privacy', models.CharField(blank=True, choices=[('', '---------'), ('IH', 'Inherit'), ('PU', 'Public'), ('PR', 'Private')], max_length=2)),
                ('send_copy', models.CharField(blank=True, default='', max_length=255, verbose_name='Send copy to')),
                ('is_deleted', models.BooleanField(blank=True, default=False, help_text='The answer is deleted?', verbose_name='Deleted')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(help_text='Answer added by user', on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='NotficationContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Contact name', max_length=100)),
                ('number', models.CharField(help_text='Contact Number', max_length=100)),
                ('priority', models.CharField(choices=[('H', 'High'), ('L', 'Low')], default='H', help_text='Priority', max_length=1)),
                ('enabled', models.BooleanField(default=True, verbose_name='Is Enabled?')),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('category', models.CharField(choices=[('', 'Select a category'), ('IN', 'Installation'), ('OA', 'Outages'), ('SO', 'Single Sign-On'), ('AU', 'Authentication'), ('AZ', 'Authorization'), ('AM', 'Access Management'), ('UG', 'Upgrade'), ('MT', 'Maintenance'), ('IM', 'Identity Management'), ('CZ', 'Customization'), ('FR', 'Feature Request'), ('LO', 'Logout'), ('OH', 'Other')], default='', max_length=2)),
                ('company', models.CharField(blank=True, max_length=20, null=True, verbose_name='Company Association')),
                ('status', models.CharField(choices=[('', 'Select a Status'), ('NW', 'New'), ('AS', 'Assigned'), ('IP', 'In Progress'), ('PI', 'Pending Input'), ('CL', 'Closed')], default='', max_length=2)),
                ('issue_type', models.CharField(choices=[('', 'Please specify the kind of issue you have encountered'), ('PO', 'Production Outage'), ('PI', 'Production Impaired'), ('PP', 'Pre-Production Issue'), ('MI', 'Minor Issue'), ('NI', 'New Development Issue')], default='', max_length=2)),
                ('server_version', models.CharField(choices=[('', 'Select Gluu Server Version'), ('3.1.2', 'Gluu Server 3.1.2'), ('3.1.1', 'Gluu Server 3.1.1'), ('3.1.0', 'Gluu Server 3.1.0'), ('3.0.2', 'Gluu Server 3.0.2'), ('3.0.1', 'Gluu Server 3.0.1'), ('2.4.4.3', 'Gluu Server 2.4.4.3'), ('2.4.4.2', 'Gluu Server 2.4.4.2'), ('2.4.4', 'Gluu Server 2.4.4'), ('2.4.3', 'Gluu Server 2.4.3'), ('2.4.2', 'Gluu Server 2.4.2'), ('Other', 'Other')], default='', help_text='Gluu Server Version', max_length=10)),
                ('server_version_comments', models.CharField(blank=True, help_text='Gluu Server Version Comments', max_length=30, null=True)),
                ('os_version', models.CharField(choices=[('', 'Select Operating System'), ('UT', 'Ubuntu'), ('CO', 'CentOS'), ('RH', 'RHEL'), ('DB', 'Debian')], default='', help_text='Which OS are you using?', max_length=2, verbose_name='OS')),
                ('os_version_name', models.CharField(max_length=10, verbose_name='OS Version')),
                ('answers_no', models.IntegerField(blank=True, default=0, verbose_name='Answers number')),
                ('link', models.URLField(blank=True, max_length=255, verbose_name='Link URL')),
                ('send_copy', models.CharField(blank=True, max_length=255, verbose_name='Send copy to')),
                ('is_private', models.BooleanField(blank=True, default=False, verbose_name='Private')),
                ('is_deleted', models.BooleanField(blank=True, default=False, verbose_name='Deleted')),
                ('os_type', models.BooleanField(blank=True, default=False, help_text='Is it 64-bit hardware?')),
                ('ram', models.BooleanField(blank=True, default=False, help_text='Does the server have at least 4GB RAM?')),
                ('visits', models.IntegerField(blank=True, default=0, verbose_name='Ticket visits')),
                ('meta_keywords', models.CharField(blank=True, max_length=500, null=True)),
                ('set_default_gluu', models.BooleanField(blank=True, default=False, verbose_name='Default Gluu')),
                ('is_notified', models.BooleanField(default=False, help_text='Indicate this ticket would be notified to admin')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by_tickets', to=settings.AUTH_USER_MODEL)),
                ('created_for', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_for_tickets', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_by_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Last Updated by')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TicketAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to='upload/')),
                ('file_src', models.TextField(blank=True, verbose_name='File Source')),
                ('is_deleted', models.BooleanField(blank=True, default=False, help_text='The document has been deleted?', verbose_name='Deleted')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='tickets.Answer')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='tickets.Ticket')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='TicketHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changed_field', models.CharField(max_length=100)),
                ('before_value', models.TextField(blank=True, null=True)),
                ('after_value', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changes', to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='tickets.Ticket')),
            ],
            options={
                'verbose_name': 'Ticket History',
                'verbose_name_plural': 'Tickets History',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='TicketNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_subscribed', models.BooleanField(default=True, help_text='Indicate whether user subscribe to notification')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacklist', to='tickets.Ticket')),
                ('user', models.ForeignKey(help_text='User associated with this ticket notification', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TicketProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(blank=True, choices=[('', 'Select a Product'), ('OD', 'OXD'), ('SG', 'Super Gluu'), ('CM', 'Cluster Manager')], max_length=2)),
                ('version', models.CharField(blank=True, choices=[('', 'Select Product Version'), ('3.1.1', '3.1.1'), ('3.0.2', '3.0.2'), ('3.0.1', '3.0.1'), ('2.4.4.3', '2.4.4.3'), ('2.4.4.2', '2.4.4.2'), ('2.4.4', '2.4.4'), ('2.4.3', '2.4.3'), ('2.4.2', '2.4.2'), ('1.0', '1.0'), ('Alpha', 'Alpha'), ('Other', 'Other')], max_length=10, verbose_name='Product Version')),
                ('os_version', models.CharField(blank=True, choices=[('', 'Select Operating System'), ('UT', 'Ubuntu'), ('CO', 'CentOS'), ('RH', 'RHEL'), ('DB', 'Debian'), ('AD', 'Android'), ('IO', 'iOS'), ('BO', 'Both')], max_length=2, verbose_name='Product OS Version')),
                ('os_version_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='Product OS Version')),
                ('ios_version_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='iOS Version')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='tickets.Ticket')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='tickets.Ticket'),
        ),
        migrations.AlterUniqueTogether(
            name='ticketnotification',
            unique_together={('ticket', 'user')},
        ),
    ]
