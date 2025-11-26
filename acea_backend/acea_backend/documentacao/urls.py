# Arquivo: documentacao/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets 

router = DefaultRouter()
router.register(r'api/pagamentos', viewsets.PagamentoViewSet)
router.register(r'api/doacoes', viewsets.DoacaoViewSet)
router.register(r'api/documentos', viewsets.DocumentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]