from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Usuario, Proyecto, Rol
from .forms import ProyectoForm, AsignarUsuariosProyectoForm
import uuid


def home(request):
    return render(request, "login/index.html")


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
    return render(request, "login/listar_usuarios.html", {'usuarios': usuarios})


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


def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('listar_usuarios')


def edicionUsuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, "login/editar_usuario.html", {"usuario": usuario})


def editar_usuario(request):
    nombre = request.POST['nombre']
    email = request.POST['email']
    telefono = request.POST['telefono']
    id_usuario = request.POST['id_usuario']
    usuario = get_object_or_404(Usuario, id=id_usuario)
    usuario.nombre = nombre
    usuario.email = email
    usuario.telefono = telefono
    usuario.save()
    return redirect('listar_usuarios')


def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            # función para generar un BACKLOG ID único
            proyecto.backlog_id = generar_backlog_id()
            proyecto.save()
            # Asignar usuarios al proyecto
            product_owner = form.cleaned_data.get('product_owner')
            scrum_master = form.cleaned_data.get('scrum_master')
            team_members = form.cleaned_data.get('team_members')
            proyecto.product_owner = product_owner
            proyecto.scrum_master = scrum_master
            for team_member in team_members:
                proyecto.team_members.add(team_member)
            # Asignar roles a los usuarios
            Rol.objects.create(usuario=product_owner, proyecto=proyecto, rol='PO')
            Rol.objects.create(usuario=scrum_master, proyecto=proyecto, rol='SM')
            for team_member in team_members:
                Rol.objects.create(usuario=team_member, proyecto=proyecto, rol='TM')
            messages.success(request, 'El proyecto ha sido creado exitosamente.')
            return redirect('proyecto_detalle', proyecto.id)
    else:
        form = ProyectoForm()
    return render(request, 'crear_proyecto.html', {'form': form})

def asignar_usuarios_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = AsignarUsuariosProyectoForm(request.POST)
        if form.is_valid():
            product_owner = form.cleaned_data.get('product_owner')
            scrum_master = form.cleaned_data.get('scrum_master')
            team_members = form.cleaned_data.get('team_members')
            proyecto.product_owner = product_owner
            proyecto.scrum_master = scrum_master
            proyecto.team_members.clear()
            for team_member in team_members:
                proyecto.team_members.add(team_member)
            # Asignar roles a los usuarios
            Rol.objects.filter(proyecto=proyecto, rol='PO').update(usuario=product_owner)
            Rol.objects.filter(proyecto=proyecto, rol='SM').update(usuario=scrum_master)
            Rol.objects.filter(proyecto=proyecto, rol='TM').delete()
            for team_member in team_members:
                Rol.objects.create(usuario=team_member, proyecto=proyecto, rol='TM')
            messages.success(request, 'Los usuarios han sido asignados al proyecto exitosamente.')
            return redirect('proyecto_detalle', proyecto.id)
    else:
        form = AsignarUsuariosProyectoForm(initial={
            'product_owner': proyecto.product_owner,
            'scrum_master': proyecto.scrum_master,
            'team_members': proyecto.team_members.all()
        })
    return render(request, 'asignar_usuarios_proyecto.html', {'form': form, 'proyecto': proyecto})

def proyecto_detalle(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    return render(request, 'proyecto_detalle.html', {'proyecto': proyecto})

def generar_backlog_id():
    return str(uuid.uuid4().hex)[:10]