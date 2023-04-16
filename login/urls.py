from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
   # path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('crear_usuario', views.crear_usuario, name="crear_usuario"),
    path('listar_usuarios', views.listar_usuarios, name="listar_usuarios"),
    path('eliminar_usuario/<usuario_id>', views.eliminar_usuario, name="eliminar_usuario"),
    path('edicionUsuario/<usuario_id>', views.edicionUsuario, name="edicionUsuario"),
    path('volver_home', views.volver_home, name=""),
    path('editar_usuario', views.editar_usuario, name="editar_usuario"),
]