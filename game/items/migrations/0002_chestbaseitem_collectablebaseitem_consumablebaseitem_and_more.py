# Generated by Django 4.2.13 on 2024-05-19 04:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChestBaseItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.item')),
                ('probability_weight', models.DecimalField(decimal_places=4, default=1.0, max_digits=6)),
                ('min_items', models.PositiveIntegerField(default=2)),
                ('max_items', models.PositiveIntegerField(default=5)),
                ('monster_guarantee', models.PositiveIntegerField(default=0)),
                ('exclude_consumables', models.BooleanField(default=False)),
                ('exclude_currency', models.BooleanField(default=False)),
                ('exclude_moves', models.BooleanField(default=False)),
                ('exclude_monsters', models.BooleanField(default=False)),
                ('exclude_wearables', models.BooleanField(default=False)),
                ('exclude_collectables', models.BooleanField(default=False)),
                ('exclude_chests', models.BooleanField(default=False)),
                ('exclude_slugup', models.BooleanField(default=False)),
                ('exclude_slugconsumable', models.BooleanField(default=False)),
            ],
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='CollectableBaseItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.item')),
            ],
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='ConsumableBaseItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.item')),
                ('health', models.PositiveIntegerField(default=0)),
                ('experience', models.PositiveIntegerField(default=0)),
            ],
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='CurrencyBaseItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.item')),
                ('min', models.PositiveIntegerField(default=10)),
                ('max', models.PositiveIntegerField(default=50)),
            ],
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='MoveBaseItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.item')),
                ('damage', models.PositiveIntegerField(default=0)),
                ('total_pp', models.PositiveIntegerField(default=0)),
                ('type_1', models.CharField(choices=[('fire', 'fire'), ('water', 'water'), ('grass', 'grass'), ('electric', 'electric'), ('ice', 'ice'), ('poison', 'poison'), ('ground', 'ground'), ('dark', 'dark'), ('steal', 'steal'), ('fairy', 'fairy'), ('normal', 'normal')], max_length=20)),
                ('type_2', models.CharField(choices=[('fire', 'fire'), ('water', 'water'), ('grass', 'grass'), ('electric', 'electric'), ('ice', 'ice'), ('poison', 'poison'), ('ground', 'ground'), ('dark', 'dark'), ('steal', 'steal'), ('fairy', 'fairy'), ('normal', 'normal')], max_length=20)),
                ('effect_1_chance', models.DecimalField(decimal_places=4, default=1.0, max_digits=6)),
                ('effect_2_chance', models.DecimalField(decimal_places=4, default=1.0, max_digits=6)),
            ],
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='SlugBaseItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.item')),
            ],
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='SlugConsumableBaseItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.item')),
                ('health', models.PositiveIntegerField(default=0)),
                ('experience', models.PositiveIntegerField(default=0)),
                ('revive', models.BooleanField(blank=True, default=False, null=True)),
            ],
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='SlugUpBaseItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.item')),
                ('attack', models.IntegerField(default=0)),
                ('sp_attack', models.IntegerField(default=0)),
                ('defense', models.IntegerField(default=0)),
                ('sp_defense', models.IntegerField(default=0)),
                ('speed', models.IntegerField(default=0)),
                ('evasion', models.IntegerField(default=0)),
                ('accuracy', models.IntegerField(default=0)),
            ],
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='WearableBaseItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.item')),
                ('type', models.CharField(choices=[('fire', 'fire'), ('water', 'water'), ('grass', 'grass'), ('electric', 'electric'), ('ice', 'ice'), ('poison', 'poison'), ('ground', 'ground'), ('dark', 'dark'), ('steal', 'steal'), ('fairy', 'fairy'), ('normal', 'normal')], max_length=20)),
                ('wearable_type', models.CharField(choices=[('show', 'show'), ('offense', 'offense'), ('defense', 'defense')], default='show', max_length=20)),
                ('health', models.PositiveIntegerField(default=0)),
                ('attack', models.PositiveIntegerField(default=0)),
                ('sp_attack', models.PositiveIntegerField(default=0)),
                ('defense', models.PositiveIntegerField(default=0)),
                ('sp_defense', models.PositiveIntegerField(default=0)),
                ('speed', models.PositiveIntegerField(default=0)),
                ('evasion', models.PositiveIntegerField(default=0)),
                ('accuracy', models.PositiveIntegerField(default=0)),
            ],
            bases=('items.item',),
        ),
    ]
