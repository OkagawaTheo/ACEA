from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

class TAlunoViewSet(viewsets.ModelViewSet):
    queryset = TAluno.objects.all()
    serializer_class = TAlunoSerializer

class TProfessorViewSet(viewsets.ModelViewSet):
    queryset = TProfessor.objects.all()
    serializer_class = TProfessorSerializer


class TPresidenteViewSet(viewsets.ModelViewSet):
    queryset = TPresidente.objects.all()
    serializer_class = TPresidenteSerializer