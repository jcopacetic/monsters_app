# Generated by Django 4.2.13 on 2024-05-19 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0003_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created_at']},
        ),
    ]
