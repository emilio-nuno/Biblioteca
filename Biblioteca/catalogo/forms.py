import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import InstanciaLibro

class FormularioRenovacionLibro(forms.Form):
    fecha_renovacion = forms.DateField(help_text="Ingrese una fecha entre ahora y 4 semanas (predeterminado 3).")

    def clean_fecha_renovacion(self):
        data = self.cleaned_data['fecha_renovacion']

        #Checamos que la fecha no sea anterior a la actual
        if data < datetime.date.today():
            raise ValidationError(_('Fecha inválida - renovación en el pasado'))

        #Checamos que la fecha no sea posterior a 4 semanas
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Fecha inválida - renovación con más de 4 semanas de antelación'))

        #Retornamos los datos limpios
        return data

"""Create a class to model a InstanciaLibro as a form"""
class FormularioCrearInstanciaLibro(forms.ModelForm):
    class Meta:
        model = InstanciaLibro
        fields = ['libro', 'sello']

class FormularioEditarInstanciaLibro(forms.ModelForm):
    class Meta:
        model = InstanciaLibro
        fields = ['libro', 'sello']