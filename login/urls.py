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
    path('listar_usuarios', views.listar_usuarios, name="listar_usuarios"),
    path('listar_proyectos',views.listar_proyectos, name="listar_proyectos"),
    path('eliminar_usuario/<usuario_id>', views.eliminar_usuario, name="eliminar_usuario"),
    path('eliminar_proyecto/<proyecto_id>', views.eliminar_proyecto, name="eliminar_proyecto"),
    path('edicionUsuario/<usuario_id>', views.edicionUsuario, name="edicionUsuario"),
    path('edicionProyecto/<proyecto_id>', views.edicionProyecto, name="edicionProyecto"),
    path('editar_proyecto', views.editar_proyecto, name="editar_proyecto"),
    path('volver_home', views.volver_home, name="volver_home"),
    path('editar_usuario', views.editar_usuario, name="editar_usuario"),
]