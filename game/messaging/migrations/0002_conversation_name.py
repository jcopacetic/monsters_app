# Generated by Django 4.2.13 on 2024-05-20 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='name',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
