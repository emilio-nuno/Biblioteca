import safedelete.models
from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
from safedelete.models import SafeDeleteModel

#TODO: Arreglar el bug donde la instancia de libro no deja eliminar el libro aunque se encuentre la instanca eliminada
class Autor(SafeDeleteModel):
    """Model representing an author."""

    primer_nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_defuncion = models.DateField('Murió', null=True, blank=True)

    class Meta:
        ordering = ['primer_nombre', 'apellido']

    def get_absolute_url(self):
        """Retorna el url para acceder al detalle del registro."""
        return reverse('detalle-autor', args=[str(self.id)])

    def __str__(self):
        """Cadena que representa al objeto."""
        return f'{self.apellido}, {self.primer_nombre}'

class Genero(SafeDeleteModel):
    """Un modelo que representa el género de un libro."""

    nombre = models.CharField(max_length=200, help_text='Inserta un género de libro (e.g. Ciencia Ficción)')

    def __str__(self):
        """Cadena que representa al modelo."""
        return self.nombre


class Libro(SafeDeleteModel):
    """Modelo que representa a un libro (pero no una copia específica)."""
    _safedelete_policy = safedelete.models.SOFT_DELETE_CASCADE

    titulo = models.CharField(max_length=200)

    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True)

    resumen = models.TextField(max_length=1000, help_text='Inserta una breve descripción del libro')
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13 caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genero = models.ManyToManyField(Genero, help_text='Selecciona uno o varios géneros para este libro')

    def __str__(self):
        """Cadena que representa al modelo."""
        return self.titulo

    def get_absolute_url(self):
        """Retorna un url para acceder al detalle del registro."""
        return reverse('book-detail', args=[str(self.id)])


class InstanciaLibro(SafeDeleteModel):
    """Modelo que representa una copia específica de un libro (e.g. que puede ser prestado de la biblioteca)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Identificador único para este libro particular en toda la biblioteca')
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE, null=True)
    sello = models.CharField(max_length=200)
    fecha_entrega = models.DateField(null=True, blank=True)
    prestatario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    ESTADO_PRESTAMO = (
        ('m', 'Mantenimiento'),
        ('p', 'En Prestamo'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    estado = models.CharField(
        max_length=1,
        choices=ESTADO_PRESTAMO,
        blank=True,
        default='m',
        help_text='Disponibilidad del libro',
    )

    # Nótese que es muy importante definir un ordenamiento para usar la función de book.bookinstance__set ya que el objeto de paginación lo necesita para saber que están en el orden correcto
    """
    Si no quieres definir ordenamiento en el modelo estas son las alternativas:

    Add a ordering inside a class Meta declaration on your model.
    Add a queryset attribute in your custom class-based view, specifying an order_by().
    Adding a get_queryset method to your custom class-based view and also specify the order_by().¿
    """

    class Meta:
        ordering = ['fecha_entrega']
        permissions = (("puede_marcar_retornado", "Marcar libro como retornado"),)

    def __str__(self):
        """Cadena que representa al modelo."""
        return f'{self.id} ({self.libro.titulo})'

    @property
    def esta_atrasado(self):
        if self.fecha_entrega and date.today() > self.fecha_entrega:
            return True
        return False
