from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
   # path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('crear_usuario', views.crear_usuario, name="crear_usuario"),
    path('crear_proyecto', views.crear_proyecto, name="crear_proyecto"),
    path('crear_us/<sprint_id>', views.crear_us, name="crear_us"),
    path('crear_us_backlog/<proyect_id>', views.crear_us_backlog, name="crear_us_backlog"),
    path('listar_usuarios', views.listar_usuarios, name="listar_usuarios"),
    path('listar_proyectos',views.listar_proyectos, name="listar_proyectos"),
    path('listar_user_stories/<sprint_id>', views.listarUSdelSprint, name="listarUSdelSprint"),
    path('listar_backlog_proy/<proyect_id>', views.listar_backlog_proy, name="listar_backlog_proy"),
    path('creacionSprint/<proyecto_id>', views.creacionSprint, name="creacionSprint"),
    path('listar_sprint/<proyecto_id>', views.listar_sprint, name="listar_sprint"),
    path('eliminar_usuario/<usuario_id>', views.eliminar_usuario, name="eliminar_usuario"),
    path('eliminar_proyecto/<proyecto_id>', views.eliminar_proyecto, name="eliminar_proyecto"),
    path('eliminar_sprint/<sprint_id>', views.eliminar_sprint, name="eliminar_sprint"),
    path('eliminar_us/<us_id>', views.eliminar_us, name="eliminar_us"),
    path('edicionUsuario/<usuario_id>', views.edicionUsuario, name="edicionUsuario"),
    path('edicionSprint/<sprint_id>', views.edicionSprint, name="edicionSprint" ),
    path('edicionProyecto/<proyecto_id>', views.edicionProyecto, name="edicionProyecto"),
    path('editar_proyecto', views.editar_proyecto, name="editar_proyecto"),
    path('editar_us/<us_id>', views.editar_us, name="editar_us"),
    path('volver_home', views.volver_home, name="volver_home"),
    path('editar_usuario', views.editar_usuario, name="editar_usuario"),
]