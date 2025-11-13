from django.shortcuts import render
from django.views.generic import ListView,DetailView 
from .models import Aluno,Professor,Presidente,Administrador
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class AlunoListView(LoginRequiredMixin, ListView):
    model = Aluno
    template_name = 'pessoa/aluno_lista.html'
    context_object_name = 'alunos'


class ProfessorListView(LoginRequiredMixin,ListView):
    model = Professor
    template_name = 'Professor/'
    context_object_name = 'Professores'


# class PresidenteListView(LoginRequiredMixin,ListView):
#     model = Presidente,
#     template_name = 'Presidente/',
#     context_object_name = 'Presidentes'

# class AdministradorListView(LoginRequiredMixin,ListView):
#     model = Administrador,
#     template_name = 'Administrador/',
#     context_object_name = 'Administradores'

class AlunoDetailAccesslMixin(UserPassesTestMixin): 
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        
        aluno_pk_url = self.kwargs.get('pk') # Retorna a pk do Aluno acessado na url pessoa/alunos/<pk::int>
        
        try:
            aluno_logado = Aluno.objects.get(email=self.request.user.email)
            return aluno_logado.id_aluno == int(aluno_pk_url)
        except (Aluno.DoesNotExist,ValueError,TypeError):
            return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Sem permissão para visualizar este perfil de aluno.")

        return super().handle_no_permission()
    
class AlunoDetailView(LoginRequiredMixin,AlunoDetailAccesslMixin,DetailView):
    model = Aluno
    template_name = 'pessoa/aluno_detalhe.html'
    context_object_name = 'aluno'
    