from django.contrib import admin
from .models import Autor, Genero, Libro, InstanciaLibro
# Register your models here.

admin.site.register(Autor)
admin.site.register(Genero)
admin.site.register(Libro)

@admin.register(InstanciaLibro)
class InstanciaLibroAdmin(admin.ModelAdmin):
    list_display = ('libro', 'estado', 'prestatario', 'fecha_entrega', 'id')
    list_filter = ('estado', 'fecha_entrega')

    fieldsets = (
        (None, {
            'fields': ('libro','sello', 'id')
        }),
        ('Disponibilidad', {
            'fields': ('estado', 'fecha_entrega','prestatario')
        }),
    )
