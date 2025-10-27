from django.shortcuts import render
from django.views.generic import ListView 
from .models import Aluno
from django.contrib.auth.mixins import LoginRequiredMixin

class AlunoListView(LoginRequiredMixin, ListView):
    model = Aluno
    template_name = 'pessoas/aluno_lista.html'
    context_object_name = 'alunos'
    