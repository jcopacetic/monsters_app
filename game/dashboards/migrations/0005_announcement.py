# Generated by Django 4.2.13 on 2024-05-19 01:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
        ('dashboards', '0004_alter_notification_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('read', models.BooleanField(blank=True, default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('base_announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_announcements', to='management.systemannouncement')),
                ('dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='dashboards.dashboard')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
