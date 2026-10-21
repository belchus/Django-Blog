#forms.ModelForm 

#forms.Form

from django import forms


class ContactoForm(forms.Form):
    nombre = forms.CharField( label ="Tu nombre", widget = forms.TextInput(attrs=
                                                                                          {"class":"form-control",
                                                                                           "placeholder":"Ingresa tu nombre"}))

    correo = forms.EmailField(label = "Tu correo electronico", widget=forms.EmailInput(attrs={"class":"form-control",
                                                                                              "placeholder":"tucorreo@gmail.com"}))
    mensaje = forms.CharField(min_length=10,label= "Tu mensaje",widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Escribe tu mensaje.."}))