# Generated by Django 3.1.4 on 2021-01-15 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
