# Generated by Django 4.1.7 on 2023-04-29 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('backlog_id', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_rol', models.CharField(choices=[('PO', 'Product Owner'), ('SM', 'Scrum Master'), ('TM', 'Team Member')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioProyecto',
            fields=[
                ('id_usu_proy_rol', models.AutoField(primary_key=True, serialize=False)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.proyecto')),
                ('rol_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.rol')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.usuario')),
            ],
        ),
    ]
