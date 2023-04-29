from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Usuario, Proyecto, Rol, UsuarioProyectoRol
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "login/index.html")
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
            messages.error(request, "datos incorrectos")
            return redirect('home')

    return render(request, "login/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Saliste correctamente")
    return redirect('home')


def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "login/listar_usuarios.html", {"usuarios": usuarios})

def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST['telefono']
        try:
            usuario = Usuario(nombre=nombre, email=email, telefono=telefono)
            usuario.save()
            return redirect('listar_usuarios')
        except IntegrityError:
            error = "Ya existe un usuario con el email ingresado."
            return render(request, 'login/crear_usuario.html', {'error': error})
    else:
        return render(request, 'login/crear_usuario.html')


def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
    usuario.delete()
    return redirect('listar_usuarios')


def edicionUsuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
    return render(request, "login/editar_usuario.html", {"usuario": usuario})


def editar_usuario(request):
    nombre = request.POST['nombre']
    email = request.POST['email']
    telefono = request.POST['telefono']
    id_usuario = request.POST['id_usuario']
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    usuario.nombre = nombre
    usuario.email = email
    usuario.telefono = telefono
    usuario.save()
    return redirect('listar_usuarios')


def crear_proyecto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        if not nombre:
            messages.error(request, 'Debe proporcionar un nombre para el proyecto.')
            return redirect('crear_proyecto')

        # Verificar si ya existe un proyecto con el mismo nombre
        if Proyecto.objects.filter(nombre=nombre).exists():
            messages.error(request, f'Ya existe un proyecto con el nombre "{nombre}".')
            return redirect('crear_proyecto')

        # Limitar la longitud del nombre del proyecto
        if len(nombre) > 100:
            messages.error(request, 'El nombre del proyecto debe tener como máximo 100 caracteres.')
            return redirect('crear_proyecto')

        proyecto = Proyecto(nombre=nombre)
        proyecto.save()
        messages.success(request, 'El proyecto ha sido creado exitosamente.')
        return redirect('listar_proyectos')
    else:
        return render(request, 'login/crear_proyecto.html')
    
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, backlog_id=proyecto_id)
    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, 'Proyecto eliminado exitosamente')
        return redirect('listar_proyectos')
    else:
        return render(request, 'login/confirmar_eliminar_proyecto.html', {'proyecto': proyecto})


def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, backlog_id=proyecto_id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if not nombre:
            messages.error(request, 'Debe proporcionar un nombre para el proyecto.')
            return redirect('editar_proyecto', proyecto_id=proyecto_id)

        # Verificar si ya existe un proyecto con el mismo nombre
        if Proyecto.objects.filter(nombre=nombre).exclude(backlog_id=proyecto.backlog_id).exists():
            messages.error(request, f'Ya existe un proyecto con el nombre "{nombre}".')
            return redirect('editar_proyecto', proyecto_id=proyecto_id)

        # Limitar la longitud del nombre del proyecto
        if len(nombre) > 100:
            messages.error(request, 'El nombre del proyecto debe tener como máximo 100 caracteres.')
            return redirect('editar_proyecto', proyecto_id=proyecto_id)

        proyecto.nombre = nombre
        proyecto.save()
        messages.success(request, f'El proyecto "{proyecto.nombre}" ha sido actualizado correctamente.')
        return redirect('listar_proyectos')
    
    return render(request, "login/editar_proyecto.html", {"proyecto": proyecto})

def listar_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, "login/listar_proyectos.html", {'proyectos': proyectos})

def confirmar_eliminacion_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, backlog_id=proyecto_id)

    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, 'Proyecto eliminado exitosamente')
        return redirect('listar_proyectos')

    context = {'proyecto': proyecto}
    return render(request, 'login/confirmar_eliminacion_proyecto.html', context)

# Asignación de usuarios a proyectos

def asignar_usuario_proyecto_rol(request):
    # Verificar si la tabla ya contiene los registros de los roles
    if not Rol.objects.filter(nombre='Scrum Master').exists():
        # Crear registro del rol de Scrum Master
        Rol.objects.create(nombre='Scrum Master')

    if not Rol.objects.filter(nombre='Product Owner').exists():
        # Crear registro del rol de Product Owner
        Rol.objects.create(nombre='Product Owner')

    if not Rol.objects.filter(nombre='Team Member').exists():
        # Crear registro del rol de Team Member
        Rol.objects.create(nombre='Team Member')
        
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        backlog_id = request.POST.get('backlog_id')
        nombre_rol = request.POST.get('nombre_rol')
        
        usuario = Usuario.objects.get(pk=id_usuario)
        proyecto = Proyecto.objects.get(pk=backlog_id)
        rol = Rol.objects.get(nombre=nombre_rol)
        
        usuario_proyecto_rol = UsuarioProyectoRol(
            id_usuario=usuario,
            backlog_id=proyecto,
            idRol=rol
        )
        usuario_proyecto_rol.save()
        
        return render(request, 'login/asignacion_exitosa.html')
        
    # Obtener la lista de usuarios, proyectos y roles para mostrar en las opciones
    usuarios = Usuario.objects.all()
    proyectos = Proyecto.objects.all()
    roles = Rol.objects.all()
    
    context = {'usuarios': usuarios, 'proyectos': proyectos, 'roles': roles}
    return render(request, 'login/asignar_usuario_proyecto_rol.html', context)

@login_required(login_url='/signin')
def lista_usuarios_proyectos_roles(request):
    usuarios = Usuario.objects.all()
    proyectos = Proyecto.objects.all()
    roles = UsuarioProyectoRol.objects.all()
    context = {'usuarios': usuarios, 'proyectos': proyectos, 'roles': roles}
    return render(request, 'login/lista_usuarios_proyectos_roles.html', context)
'''
def crear_rol(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        
        rol = Rol(
            nombre=nombre,
            descripcion=descripcion
        )
        rol.save()
        
        return render(request, 'login/asignacion_exitosa.html')
'''