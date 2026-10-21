from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ContactoForm
from .models import Autor, Comentario, Post

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

def nuevo_post(request):
    autores = Autor.objects.all()

    if request.method == "POST":

        titulo = request.POST["titulo"]
        contenido = request.POST["contenido"]
        autor_id = request.POST["autor"]
        autor = Autor.objects.get(id=autor_id)
        imagen = request.FILES.get("imagen")

        post = Post(titulo=titulo,autor=autor,contenido=contenido,imagen=imagen)

        post.save()

        return redirect("lista_posts")

    return render(request, "nuevo_post.html", {"autores":autores})


# --------------------------------------------------
# EDITAR POST
# --------------------------------------------------

def editar_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)


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

def eliminar_post(request, post_id):

    post = get_object_or_404(Post, id= post_id)
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

def dejar_comentario(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == "POST":
        contenido = request.POST.get("contenido")
        Comentario.objects.create(contenido = contenido,post = post)
        return redirect("detalle_post",post_id = post.id)
    
    return render(request,"dejar_comentario.html",{"post":post})