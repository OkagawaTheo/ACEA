from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views      # Para as views antigas (HTML)
from . import viewsets   # IMPORTANTE: Importando os viewsets da API
from .auth_views import CustomAuthToken

# --- Configuração da API (Router) ---
router = DefaultRouter()
router.register(r'api/alunos', viewsets.AlunoViewSet)
router.register(r'api/professores', viewsets.ProfessorViewSet)
router.register(r'api/presidentes', viewsets.PresidenteViewSet)
router.register(r'api/administradores', viewsets.AdministradorViewSet)
router.register(r'api/doadores', viewsets.DoadorViewSet)

urlpatterns = [
    # --- Rotas da API (Novas) ---
    path('', include(router.urls)), # Isso habilita todas as rotas acima automaticamente

    # --- Rotas Antigas (Mantivemos por segurança) ---
    path("alunos_lista/", views.AlunoListView.as_view(), name="aluno_lista"),
    path("alunos_detalhe/<int:pk>/", views.AlunoDetailView.as_view(), name="aluno_detalhe"),
    path("alunos_pagamentos/<int:pk>/pagamentos", views.AlunoPagamentosView.as_view(), name="aluno_pagamentos"),
    path('api/login/', CustomAuthToken.as_view())
]