# Generated by Django 4.1.7 on 2023-05-14 22:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_alter_sprint_fecha_fin_prevista_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='fecha_fin_prevista',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 28, 18, 52, 27, 590386)),
        ),
    ]