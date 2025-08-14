from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.db import models
from django import forms
from .forms import CategoriaForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Pagina
from .models import Post, Comentario, Categoria
from .forms import PostForm, ComentarioForm, RegistroForm, ContactoForm
from django.contrib.auth import login


# Lista de posts públicos, paginada, con filtros
class PostListView(ListView):
    model = Post
    template_name = 'mundial/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.filter(publicado=True, is_deleted=False)

        # --- Filtrar por fecha ---
        fecha = self.request.GET.get('fecha')
        if fecha:
            queryset = queryset.filter(fecha_publicacion__date=fecha)

        # --- Filtrar por categoría ---
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria__id=categoria_id)

        # --- Filtrar por cantidad de comentarios ---
        comentarios_min = self.request.GET.get('comentarios')
        if comentarios_min:
            queryset = queryset.annotate(num_comentarios=models.Count('comentarios')).filter(num_comentarios__gte=comentarios_min)

        return queryset.order_by('-fecha_publicacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


# Detalle de un post y sus comentarios
class PostDetailView(DetailView):
    model = Post
    template_name = 'mundial/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = self.object.comentarios.filter(aprobado=True).order_by('-fecha')
        context['form_comentario'] = ComentarioForm()
        return context


# Crear un post (solo usuario logueado)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'mundial/post_form.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


# Editar post (solo autor o admin)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'mundial/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.autor or self.request.user.is_staff
    


# --- Nueva vista para eliminar post con restricciones ---
@login_required
def eliminar_post(request, slug):
    post = get_object_or_404(Post, slug=slug, is_deleted=False)

    if not request.user.is_staff:
        if request.user != post.autor:
            messages.error(request, "No tienes permiso para eliminar este post.")
            return redirect('mundial:post_detail', slug=slug)

        dias_limite = getattr(settings, 'POST_AUTHOR_DELETE_DAYS', 7)
        if (timezone.now() - post.fecha_creacion).days > dias_limite:
            messages.error(request, f"Solo puedes eliminar posts creados en los últimos {dias_limite} días.")
            return redirect('mundial:post_detail', slug=slug)

        if post.comentarios.filter(aprobado=True).exists():
            messages.error(request, "No puedes eliminar un post con comentarios aprobados.")
            return redirect('mundial:post_detail', slug=slug)

    post.is_deleted = True
    post.deleted_at = timezone.now()
    post.save()

    messages.success(request, "El post ha sido eliminado correctamente.")
    return redirect('mundial:post_list')


# --- Vista para eliminar un post con permisos de superusuario Hernan ---
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Solo el superusuario con username "Hernan" puede eliminar
    if request.user.is_superuser and request.user.username == "Hernan":
        post.delete()
        messages.success(request, "El post fue eliminado correctamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar este post.")

    return redirect('mundial:post_list')


# Vista para agregar comentario a un post
@login_required
def agregar_comentario(request, slug):
    post = get_object_or_404(Post, slug=slug, publicado=True, is_deleted=False)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.post = post
            comentario.aprobado = True
            comentario.save()
            return redirect('mundial:post_detail', slug=slug)
    else:
        form = ComentarioForm()
    return render(request, 'mundial/agregar_comentario.html', {'form': form, 'post': post})


def acerca(request):
    pagina = Pagina.objects.filter(nombre='Acerca de nosotros').first()
    return render(request, 'mundial/acerca.html', {'pagina': pagina})



def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mundial:post_list')
    else:
        form = RegistroForm()
    return render(request, "mundial/registro.html", {"form": form})


def contacto_view(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "mundial/contacto_exito.html")
    else:
        form = ContactoForm()
    return render(request, "mundial/contacto.html", {"form": form})


@login_required
def post_eliminar_seguro(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Solo el autor o un admin puede eliminar
    if request.user != post.autor and not request.user.is_staff:
        messages.error(request, "No tienes permiso para eliminar este post.")
        return redirect('mundial:post_detail', slug=slug)

    if request.method == "POST":
        post.delete()
        messages.success(request, "El post fue eliminado correctamente.")
        return redirect('mundial:post_list')

    # Si es GET, mostramos la confirmación
    return render(request, 'mundial/post_confirm_delete.html', {'post': post})


@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    # Verifica que el usuario es el superusuario Hernan
    if request.user.is_superuser and request.user.username == "Hernan":
        comentario.delete()
        messages.success(request, "Comentario eliminado correctamente.")
    else:
        messages.error(request, "No tienes permisos para eliminar este comentario.")

    return redirect('mundial:post_detail', slug=comentario.post.slug)


#Vista para crear categoría
@login_required
def nueva_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mundial:post_list')  # Redirige a la lista de posts
    else:
        form = CategoriaForm()
    return render(request, 'mundial/nueva_categoria.html', {'form': form})


#editar acerca de nosotros
class PaginaForm(forms.ModelForm):
    class Meta:
        model = Pagina
        fields = ['contenido']

def editar_acerca(request):
    # Busca la página, y si no existe, la crea automáticamente
    pagina, created = Pagina.objects.get_or_create(
        id=1,
        defaults={
            'nombre': 'Acerca de nosotros',
            'contenido': 'Este blog fue creado para compartir información, historia y curiosidades sobre los Mundiales de Fútbol FIFA desde 1930 hasta la actualidad.'
        }
    )

    if request.method == 'POST':
        form = PaginaForm(request.POST, instance=pagina)
        if form.is_valid():
            form.save()
            return redirect('mundial:acerca')
    else:
        form = PaginaForm(instance=pagina)

    return render(request, 'mundial/editar_acerca.html', {'form': form})

 
