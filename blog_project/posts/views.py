from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Autor, Post




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

        autor = Autor(nombre=nombre, 
                      apellido=apellido, 
                      email=email, 
                      username=username, 
                      password=password)
        
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

    return render(request,"lista_autores.html",{"autores":autores})
# --------------------------------------------------
# LISTA DE POSTS
# --------------------------------------------------

def lista_posts(request):
    posts = Post.objects.all()

    return render(request, "lista_posts.html",{"posts":posts})


# --------------------------------------------------
# DETALLE DE UN POST
# --------------------------------------------------

def detalle_post(request, post_id):
    post = Post.objects.get(id= post_id)
    return render(request,"detalle_post.html", {"post": post})
    


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

        post = Post(titulo=titulo,autor=autor,contenido=contenido)

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
    return render(request, "contacto.html")