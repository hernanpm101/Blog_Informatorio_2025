from django.urls import path
from . import views

app_name = 'mundial'

urlpatterns = [
    path('acerca/', views.acerca, name='acerca'),
    path("registro/", views.registro, name="registro"),
    path('contacto/', views.contacto_view, name='contacto'),

    path('post/nuevo/', views.PostCreateView.as_view(), name='post_create'),  # primero lo específico
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/editar/', views.PostUpdateView.as_view(), name='post_update'),

    # Eliminar normal (sin restricciones)
    path('post/<slug:slug>/eliminar/', views.post_eliminar_seguro, name='post_eliminar'),

    # Eliminar con restricciones
    path('post/<slug:slug>/eliminar-seguro/', views.eliminar_post, name='post_eliminar_seguro'),

    # Nuevo: eliminar post solo si es superusuario "Hernan"
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),

    path('post/<slug:slug>/comentar/', views.agregar_comentario, name='agregar_comentario'),
    path('comentario/<int:comentario_id>/eliminar/', views.eliminar_comentario, name='eliminar_comentario'),

    path('categoria/nueva/', views.nueva_categoria, name='nueva_categoria'),

    path('acerca/', views.acerca, name='acerca'),
    path('acerca/editar/', views.editar_acerca, name='editar_acerca'),


    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),  # lo genérico al final
]


