from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

class TPagamentoViewSet(viewsets.ModelViewSet):
    queryset = TPagamento.objects.all()
    serializer_class = TPagamentoSerializer

class TDoacaoViewSet(viewsets.ModelViewSet):
    queryset = TDoacao.objects.all()
    serializer_class = TDoacaoSerializer

class TDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TDocumento.objects.all()
    serializer_class = TDocumentoSerializer
