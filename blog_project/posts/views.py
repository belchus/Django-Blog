from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request,"inicio.html")

def base(request):
    return render(request,"base.html")

def lista_posts(request):
    
    posts = [
        {
            "id":1,
            "titulo":"Mi primer post",
            "autor": "Cami"
        },
        {
            "id":2,
            "titulo":"Mi segundo post",
            "autor": "Belu"

        },
        {
            "id":3,
            "titulo":"Mi tercer post",
            "autor": "Benicio"

        }
    ]
    contexto = {"posts":posts}
    return render(request,"lista_posts.html",contexto)

def detalle_post(request,post_id):
    return HttpResponse(f"Estas viendo el post numero {post_id}")

def contacto(request):
    return render(request,"contacto.html")