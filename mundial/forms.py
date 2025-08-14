from django import forms
from .models import Categoria, Contacto, Post, Comentario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Formulario para Post con imagen
class PostForm(forms.ModelForm):
    imagen = forms.ImageField(label="Agregar imagen", required=False)

    class Meta:
        model = Post
        fields = [
            'titulo',
            'resumen',
            'contenido',
            'categoria',
            'publicado',
            'fecha_publicacion',
            'imagen'
        ]

# Formulario para Comentario
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']

# Registro de usuario
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# Formulario de contacto
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'mensaje']

# Formulario para Categoría
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
        }
