import random
import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Rol, Usuario,Proyecto, UsuarioProyecto
from django.db.models import Prefetch

# Create your views here.
def home(request):
    return render(request,"login/index.html")
""""
def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(request,"El nombre ya existe")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,"El email ya existe")
            return redirect('home')

        if len(username)>10:
            messages.error(request, "El nombre es muy largo")

        if pass1 != pass2:
            messages.error(request, "Password no coinciden")

        if not username.isalnum():
            messages.error(request, "El nombre solo puede ser alfanumerico")
            return redirect('home')



        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Tu cuenta ha sido creado exitosamente.")

        return redirect('signin')

    return render(request, "login/signup.html")
"""
def signin(request):

    if request.method == "POST":
       username = request.POST['username']
       pass1 = request.POST['pass1']

       user = authenticate(username=username, password=pass1)

       if user is not None:
          login(request, user)
          fname = user.first_name
          return render(request, "login/index.html", {'fname': fname})

       else:
          messages.error(request,"datos incorrectos")
          return redirect('home')

    return render(request, "login/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Saliste correctamente")
    return redirect('home')


def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "login/listar_usuarios.html", {'usuarios':usuarios})

def listar_proyectos(request):
    # Cargar los objetos Proyecto con sus respectivos objetos UsuarioProyecto, Usuario y Rol
    proyectos = Proyecto.objects.all().prefetch_related(
        Prefetch('usuarioproyecto_set', queryset=UsuarioProyecto.objects.all().select_related('usuario', 'rol_usuario'))
    )
    return render(request, "login/listar_proyectos.html", {'proyectos': proyectos})

def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST['telefono']
        usuario = Usuario(nombre=nombre, email=email, telefono=telefono)
        usuario.save()
        return redirect('listar_usuarios')
    else:
        return render(request, 'login/crear_usuario.html')
    
def crear_proyecto(request):
    usuarios = Usuario.objects.all()
    context = {'usuarios': usuarios}

    if request.method == 'POST':

        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        backlog_id = generar_numero_unico()
        proyect = Proyecto(nombre=nombre,backlog_id=backlog_id,descripcion=descripcion)
        proyect.save()
        usuarios_seleccionados = request.POST.getlist('usuarios[]')
        roles_seleccionados = request.POST.getlist('roles[]')
        i = 0
        for usuario in usuarios_seleccionados:
            
            rol_usu = get_object_or_404(Rol, tipo_rol=roles_seleccionados[i])
            usuario1 = get_object_or_404(Usuario, id=usuario)
            usu_proy_rol = UsuarioProyecto.objects.create(usuario=usuario1, proyecto=proyect, rol_usuario=rol_usu)
            usu_proy_rol.save() 
            i = i+1

        return redirect('listar_proyectos')
    else:
        return render(request, 'login/crear_proyecto.html', context)

def eliminar_proyecto(request, proyecto_id):
    proyect = get_object_or_404(Proyecto, backlog_id=proyecto_id)
    proyect.delete()
    return redirect('listar_proyectos')

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('listar_usuarios')

def edicionUsuario(request,usuario_id):
    usuario = get_object_or_404(Usuario,id=usuario_id)
    return render(request,"login/editar_usuario.html", {"usuario":usuario})

def edicionProyecto(request, proyecto_id):
    proyect = Proyecto.objects.prefetch_related(
    Prefetch('usuarioproyecto_set', queryset=UsuarioProyecto.objects.select_related('usuario', 'rol_usuario'))
    ).get(backlog_id=proyecto_id)
    usuarios = Usuario.objects.all()
    return render(request,"login/editar_proyecto.html", {'proyecto': proyect,'usuarios':usuarios})

def editar_proyecto(request):
    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']
    id_proyecto = request.POST['id_proyecto']

    proyecto = get_object_or_404(Proyecto, backlog_id=id_proyecto)
    proyecto.nombre = nombre
    proyecto.descripcion = descripcion
    proyecto.save()

    UsuarioProyecto.objects.filter(proyecto=proyecto).delete()

    usuarios_seleccionados = request.POST.getlist('usuarios[]')
    roles_seleccionados = request.POST.getlist('roles[]')

    for i in range(len(usuarios_seleccionados)):
        usuario = get_object_or_404(Usuario, id=usuarios_seleccionados[i])
        rol = get_object_or_404(Rol, tipo_rol=roles_seleccionados[i])
        usu_proy_rol = UsuarioProyecto.objects.create(usuario=usuario, proyecto=proyecto, rol_usuario=rol)
        usu_proy_rol.save()
    
    return redirect('listar_proyectos')




def editar_usuario(request):
    nombre = request.POST['nombre']
    email = request.POST['email']
    telefono = request.POST['telefono']
    id_usuario = request.POST['id_usuario']
    usuario = get_object_or_404(Usuario,id=id_usuario)
    usuario.nombre = nombre
    usuario.email = email
    usuario.telefono =  telefono
    usuario.save()
    return redirect('listar_usuarios')

def volver_home(request):
    return render(request,"login/index.html")

def generar_numero_unico():
    """
    Genera un número aleatorio único utilizando la biblioteca random y uuid
    """
    return str(uuid.uuid4().int & (1<<32)-1) + str(random.randint(0, 999)).zfill(3)