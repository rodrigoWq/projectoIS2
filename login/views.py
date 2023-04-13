from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Usuario

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

def edicionUsuario(request,usuario_id):
    usuario = get_object_or_404(Usuario,id=usuario_id)
    return render(request,"login/editar_usuario.html", {"usuario":usuario})

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