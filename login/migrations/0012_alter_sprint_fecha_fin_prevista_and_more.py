# Generated by Django 4.1.7 on 2023-05-14 23:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_userstories_id_proyect_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='fecha_fin_prevista',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 28, 19, 1, 57, 538060)),
        ),
        migrations.AlterField(
            model_name='userstories',
            name='id_proyect',
            field=models.ForeignKey(default=3588921124151, on_delete=django.db.models.deletion.CASCADE, to='login.proyecto'),
        ),
    ]
