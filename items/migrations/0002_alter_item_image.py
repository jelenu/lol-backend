# Generated by Django 5.0.1 on 2024-03-19 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to='media/item_images/'),
        ),
    ]