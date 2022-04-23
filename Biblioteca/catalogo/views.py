from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

from .models import Libro, Autor, InstanciaLibro, Genero

def index(request):
    """Vista de página principal"""

    num_libros = Libro.objects.all().count()
    num_instancias = InstanciaLibro.objects.all().count()

    #Libros disponibles (status = 'a')
    num_instancias_disponibles = InstanciaLibro.objects.filter(estado__exact='d').count()

    num_autores = Autor.objects.count()

    context = {
        'num_libros': num_libros,
        'num_instancias': num_instancias,
        'num_instancias_disponibles': num_instancias_disponibles,
        'num_autores': num_autores,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class ListaLibros(generic.ListView):
    model = Libro
    context_object_name = 'libros'
    template_name = 'lista_libros.html'

class DetalleLibro(generic.DetailView):
    model = Libro
    context_object_name = 'libro'
    template_name = 'detalle_libro.html'

class ListaAutores(generic.ListView):
    model = Autor
    context_object_name = 'autores'
    template_name = 'lista_autores.html'

class DetalleAutor(generic.DetailView):
    model = Autor
    context_object_name = 'autor'
    template_name = 'detalle_autor.html'

class ListaLibrosPrestatario(LoginRequiredMixin, generic.ListView):
    """Vista genérica basada en clases que enumera libros prestados al usuario actual."""
    model = InstanciaLibro
    context_object_name = 'libros'
    template_name = 'lista_libros_prestatario.html'

    def get_queryset(self):
        """Devuelve los libros prestados al usuario actual."""
        return InstanciaLibro.objects.filter(prestatario=self.request.user).order_by('fecha_entrega')