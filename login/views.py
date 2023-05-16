import datetime
import random
import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Estado, Rol, Sprint, UserStories, Usuario,Proyecto, UsuarioProyecto
from django.db.models import Prefetch
from django.urls import reverse


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

def listarUSdelSprint(request,sprint_id):
    sprint = get_object_or_404(Sprint, sprint_backlog_id=sprint_id)
    user_stories = UserStories.objects.filter(sprint=sprint)
    usuarios_proyecto = UsuarioProyecto.objects.filter(proyecto=sprint.proyecto)
    sm=0
    for usuarioPry in usuarios_proyecto:
        if usuarioPry.rol_usuario.tipo_rol == "SM":
            sm = usuarioPry.usuario.id
    context = {
        'user_stories': user_stories,
        'sprint_id': sprint_id,
        'sm': sm
    }
    return render(request, 'login/listar_user_stories.html', context)

def listar_backlog_proy(request, proyect_id):
    proyect = get_object_or_404(Proyecto, backlog_id=proyect_id)
    user_stories = UserStories.objects.filter(proyect=proyect, sprint__isnull=True)
    usuarios_proyecto = UsuarioProyecto.objects.filter(proyecto=proyect)
    sm=0
    for usuarioPry in usuarios_proyecto:
        if usuarioPry.rol_usuario.tipo_rol == "SM":
            sm = usuarioPry.usuario.id
    context = {
        'user_stories':user_stories,
        'proyect_id':proyect_id,
        'sm':sm
    }
    return render(request, 'login/listar_backlog_proy.html',context )



def listar_sprint(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, backlog_id=proyecto_id)
    sprints = Sprint.objects.filter(proyecto=proyecto)
    return render(request,"login/listar_sprint.html", {"sprints":sprints, "proyecto_id":proyecto_id})

def creacionSprint(request, proyecto_id):
    
    if request.method == 'POST':
        nombre = request.POST['nombre']
        proyecto = get_object_or_404(Proyecto, backlog_id=proyecto_id)
        sprint = Sprint(proyecto=proyecto, nombre=nombre)
        sprint.save()
        return redirect('listar_sprint', proyecto_id=proyecto_id)
    else:
        return render(request, "login/crear_sprint.html",{"proyecto_id":proyecto_id})

def crear_us_backlog(request,proyect_id):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        hecho = request.POST.get('hecho')
        story_points = request.POST.get('story_points')
        prioridad = request.POST.get('prioridad')
        estado_id = request.POST.get('estado')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        estado = get_object_or_404(Estado, estado=estado_id)
        proyect = get_object_or_404(Proyecto,backlog_id=proyect_id)
        usuarios_seleccionados = request.POST.getlist('usuarios[]')
        if len(usuarios_seleccionados)>0:
            for usuario in usuarios_seleccionados:
                usu = get_object_or_404(Usuario,id=usuario)
                usuario_proyecto = get_object_or_404(UsuarioProyecto, usuario=usu, proyecto=proyect)
                
                # Crear la instancia del UserStory
                user_story = UserStories.objects.create(
                    usuario_proyecto=usuario_proyecto,
                    proyect=proyect,
                    nombre=nombre,
                    descripcion=descripcion,
                    hecho=hecho,
                    story_points=story_points,
                    prioridad=prioridad,
                    estado=estado,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )
                user_story.save()

        else:
                if estado_id !="doing":
                    user_story = UserStories.objects.create(
                        proyect=proyect,
                        nombre=nombre,
                        descripcion=descripcion,
                        hecho=hecho,
                        story_points=story_points,
                        prioridad=prioridad,
                        estado=estado,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin
                    )
                    user_story.save()
                else:
                    messages.error(request, 'El estado no puedo ser doing si no hay usuario asignado')
                    return redirect('crear_us_backlog', proyect_id=proyect_id)    

        # Redireccionar a otra página
        return redirect('listar_backlog_proy', proyect_id = proyect_id)
    else:
        # Obtener la lista de usuarios y sprints para mostrar en el formulario
        proyect = get_object_or_404(Proyecto,backlog_id=proyect_id)
        usuarios_proyecto = UsuarioProyecto.objects.filter(proyecto=proyect)
        # Renderizar el formulario vacío con la lista de usuarios y sprints
        return render(request, 'login/crear_us.html', {'usuarios_proyecto': usuarios_proyecto})


def crear_us(request,sprint_id):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        hecho = request.POST.get('hecho')
        story_points = request.POST.get('story_points')
        prioridad = request.POST.get('prioridad')
        estado_id = request.POST.get('estado')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        sprint = get_object_or_404(Sprint,sprint_backlog_id=sprint_id)
        estado = get_object_or_404(Estado, estado=estado_id)
        proyect = get_object_or_404(Proyecto,backlog_id=sprint.proyecto.backlog_id)
        usuarios_seleccionados = request.POST.getlist('usuarios[]')
        if len(usuarios_seleccionados)>0:
            for usuario in usuarios_seleccionados:
                usu = get_object_or_404(Usuario,id=usuario)
                usuario_proyecto = get_object_or_404(UsuarioProyecto, usuario=usu, proyecto=sprint.proyecto)
                
                # Crear la instancia del UserStory
                user_story = UserStories.objects.create(
                    usuario_proyecto=usuario_proyecto,
                    sprint=sprint,
                    proyect=proyect,
                    nombre=nombre,
                    descripcion=descripcion,
                    hecho=hecho,
                    story_points=story_points,
                    prioridad=prioridad,
                    estado=estado,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )
                user_story.save()

        else:
                if estado_id !="doing":
                    user_story = UserStories.objects.create(
                        
                        sprint=sprint,
                        proyect=proyect,
                        nombre=nombre,
                        descripcion=descripcion,
                        hecho=hecho,
                        story_points=story_points,
                        prioridad=prioridad,
                        estado=estado,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin
                    )
                    user_story.save()
                else:
                    messages.error(request, 'El estado no puedo ser doing si no hay usuario asignado')
                    return redirect('crear_us', sprint_id=sprint_id)    

        # Redireccionar a otra página
        return redirect('listarUSdelSprint', sprint_id = sprint_id)
    else:
        # Obtener la lista de usuarios y sprints para mostrar en el formulario
        
        sprint = get_object_or_404(Sprint,sprint_backlog_id=sprint_id)
        usuarios_proyecto = UsuarioProyecto.objects.filter(proyecto=sprint.proyecto)
        # Renderizar el formulario vacío con la lista de usuarios y sprints
        return render(request, 'login/crear_us.html', {'usuarios_proyecto': usuarios_proyecto, 'sprint_id': sprint_id})

def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST['telefono']

        usuario = Usuario(nombre=nombre, email=email, telefono=telefono)
        usuario.save()
        myuser = User.objects.create_user(username=nombre, email=email, password="1234")
        myuser.id = usuario.id
        myuser.save()

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

def eliminar_sprint(request,sprint_id):
    sprint = get_object_or_404(Sprint,sprint_backlog_id=sprint_id)
    proyecto_id = sprint.proyecto.backlog_id
    sprint.delete()
    return redirect('listar_sprint', proyecto_id=proyecto_id)

def eliminar_us(request,us_id):
    user_story = get_object_or_404(UserStories,id_user_story=us_id)
    sprint = user_story.sprint
    user_story.delete()
    if sprint is not None:
        return redirect('listarUSdelSprint', sprint_id=sprint.sprint_backlog_id)
    else:
        return redirect('listar_backlog_proy', proyect_id=user_story.proyect.backlog_id)
    
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    myuser = get_object_or_404(User, id=usuario_id)
    myuser.delete()
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

def edicionSprint(request, sprint_id):
    sprint = get_object_or_404(Sprint, sprint_backlog_id=sprint_id)

    if request.method == 'POST':
        # Si se ha enviado el formulario, procesar los datos aquí
        sprint.nombre = request.POST.get('nombre')
        sprint.fecha_inicio_real = request.POST.get('fecha_inicio_real')
        sprint.fecha_fin_real = request.POST.get('fecha_fin_real')
        # Actualiza el objeto Sprint en la base de datos
        sprint.save()
        return redirect('listar_sprint', proyecto_id=sprint.proyecto.backlog_id)

    return render(request, "login/editar_sprint.html",{"sprint":sprint})

def editar_us(request, us_id):

    user_story = get_object_or_404(UserStories,id_user_story=us_id)
    proyecto_id = user_story.proyect.backlog_id
    proyecto = get_object_or_404(Proyecto, backlog_id=proyecto_id)
    usuarios_proyecto = UsuarioProyecto.objects.filter(proyecto=proyecto)
    sprints_proyecto = Sprint.objects.filter(proyecto=proyecto)
    context = {
        'user_story': user_story,
        'usuarios_proyecto': usuarios_proyecto,
        'sprints_proyecto':sprints_proyecto
    }

    if request.method == 'POST':
        user_story.nombre = request.POST['nombre']
        user_story.descripcion = request.POST['descripcion']
        user_story.hecho = request.POST['hecho']
        user_story.story_points = request.POST['story_points']
        user_story.prioridad = request.POST['prioridad']
        estado_id = request.POST.get('estado')
        user_story.fecha_inicio = request.POST['fecha_inicio']
        user_story.fecha_fin = request.POST['fecha_fin']
        usuario_proyecto_id = request.POST.get('usuario_asig')
        estadoActual = get_object_or_404(Estado,estado=estado_id)
        user_story.estado = estadoActual
        if usuario_proyecto_id == 'null':
            user_story.usuario_proyecto = None
        else:
            usuario_asignado = get_object_or_404(UsuarioProyecto,id_usu_proy_rol=usuario_proyecto_id)
            user_story.usuario_proyecto = usuario_asignado
        

        if user_story.estado.estado == 'doing' and user_story.usuario_proyecto is None:
            messages.error(request, 'El User Story está en estado "doing" pero no tiene usuario asignado.')
            return redirect('editar_us', us_id=us_id)

        
      
        if user_story.sprint is not None:
            user_story.save()
            actualizar_fecha_fin_proyecto(proyecto_id)
            return redirect('listarUSdelSprint', sprint_id = user_story.sprint.sprint_backlog_id)
        else:
            sprint_asig_id = request.POST.get('sprint_asig')
            if sprint_asig_id != "null" :
                sprint_asignado = get_object_or_404(Sprint, sprint_backlog_id=sprint_asig_id)
                user_story.sprint = sprint_asignado
            user_story.save()
            actualizar_fecha_fin_proyecto(proyecto_id)
            return redirect('listar_backlog_proy', proyect_id=proyecto_id)
    
    


    return render(request, "login/editar_us.html",context)


def editar_proyecto(request):
    id_proyecto = request.POST.get('id_proyecto')
    proyecto = get_object_or_404(Proyecto, backlog_id=id_proyecto)

    if 'nombre' in request.POST:
        proyecto.nombre = request.POST['nombre']
    if 'descripcion' in request.POST:
        proyecto.descripcion = request.POST['descripcion']

    proyecto.save()

    usuarios_seleccionados = request.POST.getlist('usuarios[]')
    roles_seleccionados = request.POST.getlist('roles[]')

    usuarios_actuales = UsuarioProyecto.objects.filter(proyecto=proyecto)
    usuarios_a_eliminar = usuarios_actuales.exclude(usuario__id__in=usuarios_seleccionados)

    for usu_proy_rol in usuarios_a_eliminar:
        usu_proy_rol.delete()
    
    for usuario_id, rol_nombre in zip(usuarios_seleccionados, roles_seleccionados):
        usuario = get_object_or_404(Usuario, id=usuario_id)
        rol = get_object_or_404(Rol, tipo_rol=rol_nombre)
        UsuarioProyecto.objects.update_or_create(usuario=usuario, proyecto=proyecto, defaults={'rol_usuario': rol})

    
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

def actualizar_fecha_fin_proyecto(proyecto_id):
    proyecto = get_object_or_404(Proyecto, backlog_id=proyecto_id)
    user_stories_proyecto = UserStories.objects.filter(proyect=proyecto)
    if user_stories_proyecto.filter(estado__estado='done').count() == user_stories_proyecto.count():
        proyecto.fecha_fin = datetime.date.today()
        proyecto.save()
