from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.ListaLibros.as_view(), name='libros'),
    path('libros/<int:pk>/', views.DetalleLibro.as_view(), name='detalle-libro'),
]