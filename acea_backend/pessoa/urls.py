from django.urls import path

from . import views
from .views import AlunoListView

urlpatterns = [
    path("aluno/",views.AlunoListView.as_view(),name="aluno_lista")]
    # path("alunos/<int:pk>/", views.AlunoDetailView.as_view(), name="aluno_detalhe"),