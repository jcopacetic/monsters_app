# Generated by Django 4.2.13 on 2024-05-20 04:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0005_announcement'),
        ('messaging', '0003_alter_conversation_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversationControls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('displaying', models.BooleanField(blank=True, default=False, null=True)),
                ('minimized', models.BooleanField(blank=True, default=True, null=True)),
                ('muted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controls', to='messaging.conversation')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversation_controls', to='dashboards.dashboard')),
            ],
        ),
    ]
