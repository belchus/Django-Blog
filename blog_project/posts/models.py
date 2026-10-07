from django.db import models

# Create your models here.
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}{self.apellido}"

class Post (models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor,on_delete=models.CASCADE,related_name= "posts")
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    ESTADOS = [("borrador","Borrador"),
               ("publicado","Publicado"),
               ("archivado","Archivado")]
    estado = models.CharField(max_length=20,choices=ESTADOS,default="borrador")
    resumen = models.CharField(max_length=250,blank=True)

    def __str__(self):
        return self.titulo