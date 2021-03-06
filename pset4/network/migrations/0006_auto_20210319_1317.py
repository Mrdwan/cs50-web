# Generated by Django 3.1.7 on 2021-03-19 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210319_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='network.followers'),
        ),
        migrations.AlterField(
            model_name='user',
            name='follows',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='network.follows'),
        ),
    ]
