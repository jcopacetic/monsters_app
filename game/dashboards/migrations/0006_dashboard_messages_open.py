# Generated by Django 4.2.13 on 2024-05-27 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0005_announcement'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='messages_open',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
