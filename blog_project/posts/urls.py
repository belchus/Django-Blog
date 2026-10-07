from django.urls import path
from . import views


urlpatterns = [

    path("", views.inicio, name="inicio"),

    path(
        "posts/",
        views.lista_posts,
        name="lista_posts"
    ),

    path(
        "posts/<int:post_id>/",
        views.detalle_post,
        name="detalle_post"
    ),

    path(
        "posts/nuevo/",
        views.nuevo_post,
        name="nuevo_post"
    ),

    path(
        "posts/<int:post_id>/editar/",
        views.editar_post,
        name="editar_post"
    ),

    path(
        "posts/<int:post_id>/eliminar/",
        views.eliminar_post,
        name="eliminar_post"
    ),

    path(
        "contacto/",
        views.contacto,
        name="contacto"
    ),
     path(
        "autores/",
        views.lista_autores,
        name="lista_autores"
    ),
    path("autor/crear/",
         views.crear_autor,
         name="crear_autor")
]