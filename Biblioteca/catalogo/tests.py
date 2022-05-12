from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from .models import Autor, Genero, Libro, InstanciaLibro

class InstanciaLibroTestCase(TestCase):
    def setUp(self):
        autor = Autor.objects.create(primer_nombre='Juan', apellido='Perez')
        genero1 = Genero.objects.create(nombre='Fantasia')
        genero2 = Genero.objects.create(nombre='Aventura')
        libro = Libro.objects.create(titulo='El señor de los anillos', autor=autor)
        libro.genero.set([genero1, genero2])
        InstanciaLibro.objects.create(libro=libro)

    def test_libro_eliminado(self):
        libro = Libro.objects.get(titulo='El señor de los anillos')
        instancia = InstanciaLibro.objects.get(libro=libro)
        self.assertNotIn(instancia, InstanciaLibro.objects.deleted_only())
        libro.delete()
        self.assertIn(instancia, InstanciaLibro.objects.deleted_only())

    def test_genero_eliminado(self):
        libro = Libro.objects.get(titulo='El señor de los anillos')
        aventura = Genero.objects.get(nombre='Aventura')
        aventura.delete()
        generos = libro.genero.all()
        self.assertNotIn(aventura, generos)
        self.assertIn(aventura, Genero.objects.deleted_only())

    def test_autor_eliminado(self):
        #TODO: Checar si hay manera de que el campo autor se vuelva nulo al eliminar el autor
        libro = Libro.objects.get(titulo='El señor de los anillos')
        autor = Autor.objects.get(primer_nombre='Juan')
        autor.delete()
        self.assertEqual(libro.autor, autor)
        self.assertIn(libro.autor, Autor.objects.deleted_only())

    def test_timestamp_libro(self):
        libro = Libro.objects.get(titulo='El señor de los anillos')
        instancia = InstanciaLibro.objects.get(libro=libro)

        timestamp_editado_original = instancia.editado_en
        timestamp_creado_original = instancia.creado_en

        instancia.sello = 'Sello'
        instancia.save()

        timestamp_editado_nuevo = instancia.editado_en
        timestamp_creado_nuevo = instancia.creado_en

        self.assertNotEqual(timestamp_editado_original, timestamp_editado_nuevo)
        self.assertEqual(timestamp_creado_original, timestamp_creado_nuevo)

    def test_mayusculas_titulo(self):
        nueva_instancia = InstanciaLibro.objects.create(sello='prueba')
        self.assertEqual(nueva_instancia.sello, 'Prueba')
