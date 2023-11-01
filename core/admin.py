from django.contrib import admin
from .models import Agendamento

@admin.register(Agendamento)
class MADM(admin.ModelAdmin):
     list_display = ['nome', 'email', 'opcoes', 'horario', 'local', 'data']
