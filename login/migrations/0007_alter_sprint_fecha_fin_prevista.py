# Generated by Django 4.1.7 on 2023-05-12 21:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_alter_sprint_fecha_fin_prevista'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='fecha_fin_prevista',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 26, 17, 48, 35, 461857)),
        ),
    ]
