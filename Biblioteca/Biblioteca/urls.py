"""Biblioteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
#TODO: Verificar el proceso de reestablecimiento de contraseña
#TODO: Checar si se puede modificar el nombre de el url de la app de cuenta de django de accounts a cuentas
#TODO: Usar formularios de bootstrap para formulario de inicio de sesion
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='catalogo/', permanent=True)),
    path('catalogo/', include('catalogo.urls')),
    path('cuentas/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
