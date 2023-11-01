from django.db import models

class Agendamento(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    opcoes = models.CharField(max_length=100)
    horario = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    data = models.DateField()