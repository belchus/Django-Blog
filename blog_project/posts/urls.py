from django.contrib.auth import views as auth_views
from django.urls import path ,reverse_lazy
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
    path("posts/<int:post_id>/comentar/", views.dejar_comentario, name="dejar_comentario"),
    path("cambiar_contraseña/",auth_views.PasswordChangeView.as_view(template_name = "cambiar_contraseña.html",
                                                                     success_url = reverse_lazy("mi_perfil") ),
                                                                       name= "cambiar_contraseña" ),
    path("mensajes/",views.bandeja_entrada,name="bandeja_entrada"),
    path("mensajes/enviados",views.bandeja_enviados,name="bandeja_enviados"),
    path("mensajes/enviar",views.enviar_mensaje,name="enviar_mensaje"),
    path("mensajes/<int:mensaje_id>",views.leer_mensaje,name="leer_mensaje")


]