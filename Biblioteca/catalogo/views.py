import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
# Create your views here.
from .forms import FormularioRenovacionLibro
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

class ListaLibrosPrestados(PermissionRequiredMixin, generic.ListView):
    """Vista genérica basada en clases que enumera libros prestados en general."""
    model = InstanciaLibro
    permission_required = 'catalogo.puede_marcar_retornado'
    context_object_name = 'libros'
    template_name = 'lista_libros_prestados.html'

    def get_queryset(self):
        """Devuelve los libros prestados al usuario actual."""
        return InstanciaLibro.objects.filter(estado__exact='p').order_by('fecha_entrega')

@login_required
@permission_required('catalogo.puede_marcar_retornado', raise_exception=True)
def renovar_libro_bibliotecario(request, pk):
    """Vista para renovar un libro prestado por el usuario actual."""

    instancia = get_object_or_404(InstanciaLibro, pk=pk)
    if request.method == 'POST':
        formulario = FormularioRenovacionLibro(request.POST)
        if formulario.is_valid():
            instancia.fecha_entrega = formulario.cleaned_data['fecha_renovacion']
            instancia.save()

            return HttpResponseRedirect(reverse('todos-prestamos'))
        else:
            print(formulario.errors)
    else:
        fecha_propuesta = datetime.date.today() + datetime.timedelta(weeks=3)
        formulario = FormularioRenovacionLibro(initial={'fecha_renovacion': fecha_propuesta})

    context = {'formulario': formulario, 'instancia': instancia}
    return render(request, 'renovar_libro_bibliotecario.html', context)

def instancia_libro_to_dict(instancia):
    """Function to turn an InstanciaLibro object into a dictionary"""
    titulo = instancia.libro.titulo
    id = instancia.id

    return {'titulo': titulo,
            'id': id}

"""Function to turn a list of InstanciaLibro objects into a list of dictionaries"""

def consulta_libros_disponibles(request):
    """Vista para consultar libros disponibles."""

    libros = InstanciaLibro.objects.filter(estado__exact='d')
    libros_dict = [instancia_libro_to_dict(libro) for libro in libros]
    respuesta = {'libros': libros_dict}
    return JsonResponse(respuesta)
