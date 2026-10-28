from django.urls import path
from . import views


urlpatterns = [

    path("", views.inicio, name="inicio"),
    path("login/",views.iniciar_sesion, name= "login"),
    path("register/",views.registro,name="registro"),
    path("logout/",views.cerrar_sesion,name="logout"),
    path("posts/",views.lista_posts,name="lista_posts"),
    path("posts/<int:post_id>/",views.detalle_post,name="detalle_post"),
    path("posts/nuevo/",views.nuevo_post,name="nuevo_post"),
    path("posts/<int:post_id>/editar/",views.editar_post,name="editar_post"),
    path("posts/<int:post_id>/eliminar/",views.eliminar_post,name="eliminar_post"),
    path("contacto/",views.contacto, name="contacto"),
    path("autores/",views.lista_autores,name="lista_autores"),
    path("autor/crear/",views.crear_autor, name="crear_autor"),
    path("autor/<int:autor_id>/",views.perfil_autor, name="perfil_autor"),
    path("mi_perfil/",views.mi_perfil,name="mi_perfil"),
    path("posts/<int:post_id>/comentar/", views.dejar_comentario, name="dejar_comentario")
]