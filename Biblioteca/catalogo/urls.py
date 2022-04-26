from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.ListaLibros.as_view(), name='libros'),
    path('libros/<int:pk>/', views.DetalleLibro.as_view(), name='detalle-libro'),
    path('autores/', views.ListaAutores.as_view(), name='autores'),
    path('autores/<int:pk>/', views.DetalleAutor.as_view(), name='detalle-autor'),
    path('mislibros/', views.ListaLibrosPrestatario.as_view(), name='mis-prestamos'),
    path('libros/<uuid:pk>/renovar', views.renovar_libro_bibliotecario, name='renovar-libro-bibliotecario'),
]