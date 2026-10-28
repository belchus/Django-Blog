#forms.ModelForm 

#forms.Form
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from .models import Autor


class ContactoForm(forms.Form):
    nombre = forms.CharField( label ="Tu nombre", widget = forms.TextInput(attrs=
                                                                                          {"class":"form-control",
                                                                                           "placeholder":"Ingresa tu nombre"}))

    correo = forms.EmailField(label = "Tu correo electronico", widget=forms.EmailInput(attrs={"class":"form-control",
                                                                                              "placeholder":"tucorreo@gmail.com"}))
    mensaje = forms.CharField(min_length=10,label= "Tu mensaje",widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Escribe tu mensaje.."}))


User = get_user_model()

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,label="Nombre")
    last_name = forms.CharField(max_length=100,label="Apellido")
    email = forms.EmailField(label="Correo electronico")
    avatar = forms.ImageField(required=False,label="Foto de perfil")

    class Meta:
        model=User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email"
        ]
    def clean_username(self):
        username = self.cleaned_data["username"]

        if Autor.objects.filter(username=username).exists():
            raise ValidationError(
                "Ese nombre ya esta en uso"
            )
        return username
    
    def save(self,commit=True):
        usuario = super().save(commit=False)

        usuario.first_name = self.cleaned_data["first_name"]
        usuario.last_name = self.cleaned_data["last_name"]
        usuario.email = self.cleaned_data["email"]

        if commit:
            usuario.save()

            Autor.objects.create(
                usuario=usuario,
                nombre = usuario.first_name,
                apellido = usuario.last_name,
                email = usuario.email,
                username = usuario.username,
                avatar = self.cleaned_data.get("avatar")
            )
        return usuario
    
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Autor
        
        fields =[
            "nombre",
            "apellido",
            "email",
            "avatar",
        ]

        labels = {
            "nombre" : "Nombre",
            "apellido" : "Apellido",
            "email":"Correo electronico",
            "avatar":"Foto de perfil"
        }

        widgets = {
            "nombre":forms.TextInput(attrs={"class":"form-control"}),
            "apellido":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "avatar":forms.ClearableFileInput(attrs={"class":"form-control"})
        }