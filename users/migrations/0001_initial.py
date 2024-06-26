# Generated by Django 5.0.1 on 2024-06-03 13:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkedAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=100)),
                ('tagline', models.CharField(max_length=50)),
                ('server', models.CharField(max_length=50)),
                ('main_server', models.CharField(max_length=50)),
                ('temp_icon_id', models.IntegerField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lol_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
