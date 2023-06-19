# Generated by Django 4.1.7 on 2023-06-04 22:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_proyecto_fecha_fin_alter_sprint_fecha_fin_prevista'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='fecha_fin_prevista',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 18, 18, 42, 6, 100779)),
        ),
        migrations.AlterField(
            model_name='userstories',
            name='fecha_fin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userstories',
            name='fecha_inicio',
            field=models.DateField(blank=True, null=True),
        ),
    ]