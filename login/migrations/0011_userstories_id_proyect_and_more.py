# Generated by Django 4.1.7 on 2023-05-14 23:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_alter_sprint_fecha_fin_prevista_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstories',
            name='id_proyect',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='login.proyecto'),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='fecha_fin_prevista',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 28, 19, 0, 54, 198465)),
        ),
    ]
