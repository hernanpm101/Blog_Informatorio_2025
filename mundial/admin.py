from django.contrib import admin
from .models import Categoria, Post, Comentario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'publicado', 'fecha_publicacion')
    list_filter = ('publicado', 'categoria', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'fecha_publicacion'
    ordering = ('-fecha_publicacion',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('post', 'autor', 'aprobado', 'fecha')
    list_filter = ('aprobado',)
    search_fields = ('contenido', 'autor__username')
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)

