from django.db import models
from datetime import datetime, timedelta

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)

class Proyecto(models.Model):
    backlog_id = models.CharField(primary_key=True, max_length=10, editable=False)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Rol(models.Model):
    TIPOS_ROLES = (
        ('PO', 'Product Owner'),
        ('SM', 'Scrum Master'),
        ('TM', 'Team Member'),
    )
    tipo_rol = models.CharField(max_length=2, choices=TIPOS_ROLES)

class UsuarioProyecto(models.Model):
    id_usu_proy_rol = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    rol_usuario = models.ForeignKey(Rol, on_delete=models.CASCADE)


"""    
class Sprint(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_inicio_prevista = models.DateTimeField(default=datetime.now)
    fecha_fin_prevista = models.DateTimeField(default=datetime.now() + timedelta(weeks=2))
    fecha_inicio_real = models.DateTimeField(blank=True, null=True)
    fecha_fin_real = models.DateTimeField(blank=True, null=True)
    sprint_backlog_id = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.sprint_backlog_id:
            self.sprint_backlog_id = generar_sprint_backlog_id()
        super(Sprint, self).save(*args, **kwargs)

def generar_sprint_backlog_id():
    # Lógica para generar el Sprint_Backlog_ID, por ejemplo:
    ultimo_sprint = Sprint.objects.order_by('-sprint_backlog_id').first()
    if ultimo_sprint:
        ultimo_id = int(ultimo_sprint.sprint_backlog_id[2:])
    else:
        ultimo_id = 0
    nuevo_id = str(ultimo_id + 1).zfill(8)
    return 'SP' + nuevo_id
"""