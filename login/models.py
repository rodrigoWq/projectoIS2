from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    backlog_id = models.CharField(max_length=32)
    product_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proyectos_product_owner')
    scrum_master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proyectos_scrum_master')
    team_members = models.ManyToManyField(User, related_name='proyectos_team_member')