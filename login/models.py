from django.db import models


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)


class Proyecto(models.Model):
    backlog_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)


class Rol(models.Model):
    idRol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=2, choices=(('SM', 'Scrum Master'), ('PO', 'Product Owner'), ('TM', 'Team Member')))

class UsuarioProyectoRol(models.Model):
    id_usuario_proyecto_rol = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    backlog_id = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    idRol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    
     
