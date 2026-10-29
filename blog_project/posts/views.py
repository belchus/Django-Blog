from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout,get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import ContactoForm, EditarPerfilForm, RegistroForm
from .models import Autor, Comentario, Mensaje, Post

User = get_user_model()

# --------------------------------------------------
# REGISTRO
# --------------------------------------------------

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST,request.FILES)

        if form.is_valid():
            usuario = form.save()

            login(request,usuario)
            return redirect("inicio")
    else:
        form = RegistroForm()
    return render(request,"registro.html",{"form":form})

# --------------------------------------------------
# LOGIN
# --------------------------------------------------
def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data = request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request,usuario)
            return redirect("inicio")
    else:
        form = AuthenticationForm(request)
    return render(request,"login.html",{"form":form})
# --------------------------------------------------
# LOGOUT
# --------------------------------------------------
@require_POST
def cerrar_sesion(request):
    logout(request)

    return redirect("inicio")
# --------------------------------------------------
# INICIO
# --------------------------------------------------

def inicio(request):
    return render(request, "inicio.html")

# --------------------------------------------------
# CREAR UN AUTOR
# --------------------------------------------------
def crear_autor(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        avatar = request.FILES.get("avatar")

        autor = Autor(nombre=nombre, 
                      apellido=apellido, 
                      email=email, 
                      username=username, 
                      password=password,
                      avatar= avatar)
        
        autor.save()

        return redirect("inicio")
    return render(request,"crear_autor.html")

# --------------------------------------------------
# BASE
# --------------------------------------------------

def base(request):
    return render(request, "base.html")

# --------------------------------------------------
# LISTA DE AUTORES
# --------------------------------------------------


def lista_autores(request):
    autores = Autor.objects.all()
    busqueda = request.GET.get("buscar")
    if busqueda:
        autores = autores.filter(username__icontains = busqueda)

    return render(request,"lista_autores.html",{"autores":autores})

# --------------------------------------------------
# PERFIL DE AUTOR
# --------------------------------------------------


def perfil_autor(request,autor_id):
    autor = get_object_or_404(Autor,id = autor_id)
    posts = autor.posts.all()

    return render(request,"perfil_autor.html",{"autor":autor, "posts":posts})

# --------------------------------------------------
# EDITAR PERFIL DE AUTOR
# --------------------------------------------------
@login_required
def mi_perfil(request):
    autor = get_object_or_404(Autor,usuario=request.user)
    if request.method == "POST":
        form = EditarPerfilForm(request.POST,
                                request.FILES,
                                instance=autor)
        if form.is_valid():
            autor=form.save()

            usuario = request.user
            usuario.first_name = autor.nombre
            usuario.last_name = autor.apellido
            usuario.email = autor.email
            usuario.save()

            return redirect("mi_perfil")
        
    else:
        form = EditarPerfilForm(instance=autor)
    
    return render(request,"mi_perfil.html",{"form":form,"autor":autor})
# --------------------------------------------------
# LISTA DE POSTS
# --------------------------------------------------

def lista_posts(request):
    posts = Post.objects.all()

    busqueda = request.GET.get("buscar")
    if busqueda:
        posts = posts.filter(titulo__icontains = busqueda)
    
    estado = request.GET.get("estado")

    if estado: 
        posts = posts.filter(estado = estado)

    orden = request.GET.get("orden","reciente")
    if orden == "antiguo":
        posts = posts.order_by("fecha_creacion")
    else:
        posts = posts.order_by('-fecha_creacion')

    return render(request, "lista_posts.html",{"posts":posts,"busqueda":busqueda,"estado":estado,"orden":orden})


# --------------------------------------------------
# DETALLE DE UN POST
# --------------------------------------------------

def detalle_post(request, post_id):
    post = Post.objects.get(id= post_id)
    comentarios = post.comentarios.all()
    return render(request,"detalle_post.html", {"post": post,"comentarios":comentarios})
    


# --------------------------------------------------
# CREAR POST
# --------------------------------------------------

@login_required

def nuevo_post(request):
    autor = get_object_or_404(Autor,usuario=request.user)

    if request.method == "POST":

        titulo = request.POST["titulo"]
        contenido = request.POST["contenido"]
        imagen = request.FILES.get("imagen")

        post = Post(titulo=titulo,autor=autor,contenido=contenido,imagen=imagen)

        post.save()

        return redirect("lista_posts")

    return render(request, "nuevo_post.html")


# --------------------------------------------------
# EDITAR POST
# --------------------------------------------------
@login_required

def editar_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if post.autor.usuario_id != request.user.id:
        return redirect("lista_posts")


    if request.method == "POST":

        post.titulo = request.POST["titulo"]
        post.contenido = request.POST["contenido"]
        nueva_imagen = request.FILES.get("imagen")

        if nueva_imagen:
            post.imagen = nueva_imagen

        post.save()

        return redirect("lista_posts")

    return render(request, "editar_post.html", {
        "post": post
    })


# --------------------------------------------------
# ELIMINAR POST
# --------------------------------------------------
@login_required

def eliminar_post(request, post_id):

    post = get_object_or_404(Post, id= post_id)
    if post.autor.usuario_id != request.user.id:
        return redirect("lista_posts")
    post.delete()

    return redirect("lista_posts")


# --------------------------------------------------
# CONTACTO
# --------------------------------------------------

def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            correo = form.cleaned_data["correo"]
            mensaje = form.cleaned_data["mensaje"]
            print(f"Nombre: {nombre}")
            print(f"Correo: {correo}")
            print(f"Mensaje: {mensaje}")           
            return render(request,"contacto_exito.html",{"nombre":nombre})

    else:
        form = ContactoForm()

    return render(request, "contacto.html", {"form": form})
   
    

# --------------------------------------------------
# HACER UN COMENTARIO
# --------------------------------------------------
@login_required

def dejar_comentario(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == "POST":
        contenido = request.POST.get("contenido")
        Comentario.objects.create(contenido = contenido,post = post)
        return redirect("detalle_post",post_id = post.id)
    
    return render(request,"dejar_comentario.html",{"post":post})

# --------------------------------------------------
# BANDEJA DE ENTRADA
# --------------------------------------------------

@login_required

def bandeja_entrada(request):
    mensajes = Mensaje.objects.filter(
        destinatario= request.user).order_by("-fecha_envio")
    
    return render(request,"bandeja_entrada.html",{"mensajes":mensajes})


# --------------------------------------------------
# BANDEJA DE LEIDOS
# --------------------------------------------------

@login_required

def bandeja_enviados(request):
    mensajes = Mensaje.objects.filter(
        remitente= request.user).order_by("-fecha_envio")
    
    return render(request,"bandeja_enviados.html",{"mensajes":mensajes})

# --------------------------------------------------
# ENVIAR MENSAJE
# --------------------------------------------------

@login_required

def enviar_mensaje(request):
    usuarios = User.objects.exclude(id=request.user.id)
    if request.method == "POST":
        destinatario_id = request.POST.get("destinatario")
        asunto = request.POST.get("asunto","").strip()
        contenido = request.POST.get("contenido","").strip()

        destinatario = get_object_or_404(User,id=destinatario_id) if destinatario_id else None

        if destinatario is None or destinatario_id == request.user.id:
            messages.error (request,"Selecciona un destinatarion valido")
        elif not asunto or not contenido:
            messages.error(request,"Completa el asunto y el mensaje")
        
        else:
            Mensaje.objects.create(
                remitente = request.user,
                destinatario = destinatario,
                asunto = asunto,
                contenido = contenido
            )
            messages.success(request,"Mensaje enviado")
            return redirect("bandeja_enviados")
    return render( request,"enviar_mensaje.html",{"usuarios":usuarios})

# --------------------------------------------------
# LEER MENSAJE
# --------------------------------------------------

@login_required
def leer_mensaje(request,mensaje_id):
    mensaje = get_object_or_404(Mensaje,id=mensaje_id,destinatario=request.user)
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save(update_fields=["leido"])
    
    return render(request,"leer_mensaje.html", {"mensaje":mensaje})


