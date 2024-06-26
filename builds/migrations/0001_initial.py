# Generated by Django 5.0.1 on 2024-03-26 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('colloq', models.CharField(blank=True, max_length=255)),
                ('plaintext', models.CharField(blank=True, max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('gold_base', models.IntegerField()),
                ('gold_total', models.IntegerField()),
                ('gold_sell', models.IntegerField()),
                ('item_from', models.ManyToManyField(blank=True, related_name='crafts_into', to='builds.item')),
                ('item_into', models.ManyToManyField(blank=True, related_name='crafts_from', to='builds.item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='builds.item')),
                ('stat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='builds.stat')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='stats',
            field=models.ManyToManyField(through='builds.ItemStat', to='builds.stat'),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(to='builds.tag'),
        ),
    ]
