from django.shortcuts import render, redirect
from .form import ContatoForm
from .models import Agendamento


def contato(request):
     if(request.method) == 'POST':
          form = ContatoForm(request.POST)
          if form.is_valid():
               agendamento = Agendamento(
                    nome = form.cleaned_data['nome'],
                    email=form.cleaned_data['email'],
                    opcoes=form.cleaned_data['opcoes'],
                    horario=form.cleaned_data['horario'],
                    local=form.cleaned_data['local'],
                    data=form.cleaned_data['data'],
               )
               agendamento.save()
               form.send_email()
     else:
          form = ContatoForm()
     context = {
          'form' : form
     }
     return render(request, 'form.html', context)