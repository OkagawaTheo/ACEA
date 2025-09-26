from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

class TCursoViewSet(viewsets.ModelViewSet):
    queryset = TCurso.objects.all()
    serializer_class = TCursoSerializer

class TAtividade_esportivaViewSet(viewsets.ModelViewSet):
    queryset = TAtividade_esportiva.objects.all()
    serializer_class = TAtividade_esportiva

    
