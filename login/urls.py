from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    # Rutas para proyectos
    path('proyectos/', views.lista_proyectos, name="lista_proyectos"),
    path('proyectos/crear/', views.crear_proyecto, name="crear_proyecto"),
    path('proyectos/<int:proyecto_id>/', views.detalle_proyecto, name="proyecto_detalle"),
    path('proyectos/<int:proyecto_id>/editar/', views.editar_proyecto, name="editar_proyecto"),
    path('proyectos/<int:proyecto_id>/eliminar/', views.eliminar_proyecto, name="eliminar_proyecto"),
    # Rutas para usuarios
    path('usuarios/', views.listar_usuarios, name="listar_usuarios"),
    path('usuarios/crear/', views.crear_usuario, name="crear_usuario"),
    path('usuarios/<int:usuario_id>/', views.detalle_usuario, name="usuario_detalle"),
    path('usuarios/<int:usuario_id>/editar/', views.editar_usuario, name="editar_usuario"),
    path('usuarios/<int:usuario_id>/eliminar/', views.eliminar_usuario, name="eliminar_usuario"),
]