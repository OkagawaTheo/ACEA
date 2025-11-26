from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

# O Router cria os endereços automaticamente
router = DefaultRouter()
router.register(r'api/cursos', viewsets.CursoViewSet)
router.register(r'api/atividades', viewsets.AtividadeEsportivaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]