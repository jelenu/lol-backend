from django.contrib import admin
from django.urls import path
from prueba.views import tu_vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mi-vista/', tu_vista, name='mi_vista'),

]
