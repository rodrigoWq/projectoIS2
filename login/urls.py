from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('crear_usuario', views.crear_usuario, name="crear_usuario"),
    path('listar_usuarios', views.listar_usuarios, name="listar_usuarios"),
    path('eliminar_usuario/<usuario_id>', views.eliminar_usuario, name="eliminar_usuario"),
    path('edicionUsuario/<usuario_id>', views.edicionUsuario, name="edicionUsuario"),
    path('editar_usuario', views.editar_usuario, name="editar_usuario"),
    path('crear_proyecto', views.crear_proyecto, name="crear_proyecto"),
    path('listar_proyectos', views.listar_proyectos, name="listar_proyectos"),
    path('eliminar_proyecto/<proyecto_id>', views.eliminar_proyecto, name="eliminar_proyecto"),
    path('editar_proyecto/<proyecto_id>', views.editar_proyecto, name="editar_proyecto"),
    path('confirmar_elimacion_proyecto/<proyecto_id>', views.confirmar_eliminacion_proyecto, name="confirmar_elimacion_proyecto"),
    path('asignar_usuario_proyecto_rol/', views.asignar_usuario_proyecto_rol, name='asignar_usuario_proyecto_rol'),
    path('lista_usuarios_proyectos_roles', views.lista_usuarios_proyectos_roles, name='lista_usuarios_proyectos_roles'),
]
