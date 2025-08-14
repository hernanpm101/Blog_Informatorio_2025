from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            num = 1
            while Categoria.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    resumen = models.CharField(max_length=300, blank=True)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    imagen = models.ImageField(upload_to='posts/', blank=True, null=True)  # NUEVO
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now, null=True, blank=True)
    publicado = models.BooleanField(default=False)

    # Borrado suave
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generar slug único
        if not self.slug:
            base_slug = slugify(self.titulo)
            slug = base_slug
            num = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug

        # Asignar fecha_publicacion SOLO al pasar a publicado por primera vez
        if self.publicado and self.fecha_publicacion is None:
            self.fecha_publicacion = timezone.localtime(timezone.now())

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Borrado suave: marca el post como eliminado sin borrarlo físicamente."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    @classmethod
    def activos(cls):
        """Devuelve solo los posts que no están eliminados."""
        return cls.objects.filter(is_deleted=False)

    def get_absolute_url(self):
        return reverse('mundial:post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f'Comentario de {self.autor.username} en "{self.post.titulo}"'
    

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.email}"
    

class Pagina(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    contenido = models.TextField()

    def __str__(self):
        return self.nombre
