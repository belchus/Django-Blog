from django.contrib import admin
from .models import Autor, Comentario, Post

admin.site.register(Autor)
admin.site.register(Post)
admin.site.register(Comentario)
