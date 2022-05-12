from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.ListaLibros.as_view(), name='libros'),
    path('libros/<int:pk>/', views.DetalleLibro.as_view(), name='detalle-libro'),
    path('libros/crear/', views.CrearLibro.as_view(), name='crear-libro'),
    path('libros/<uuid:pk>/actualizar/', views.ActualizarLibro.as_view(), name='actualizar-libro'),
    path('libros/<uuid:pk>/eliminar/', views.EliminarLibro.as_view(), name='eliminar-libro'),
    path('autores/', views.ListaAutores.as_view(), name='autores'),
    path('autores/<int:pk>/', views.DetalleAutor.as_view(), name='detalle-autor'),
    path('mislibros/', views.ListaLibrosPrestatario.as_view(), name='mis-prestamos'),
    path('prestados/', views.ListaLibrosPrestados.as_view(), name='todos-prestamos'),
    path('libros/<uuid:pk>/renovar', views.renovar_libro_bibliotecario, name='renovar-libro-bibliotecario'),
    path('disponibles/', views.consulta_libros_disponibles, name='libros-disponibles'),
    path('libros/<int:pk>/cambiar-imagen', views.CambiarImagenLibro.as_view(), name='cambiar-imagen-libro'),
    path('correo/', views.mandar_correo, name='correo'),
]