from django.urls import path
from . import views

urlpatterns = [
    path("alunos/",views.AlunoListView.as_view(),name="aluno_lista"),
    path("alunos/<int:pk>/",views.AlunoDetailView.as_view(),name="aluno_detalhe")
    ]
    