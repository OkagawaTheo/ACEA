from django.shortcuts import render
from rest_framework import viewsets
from .models import TAluno
from .serializers import TAlunoSerializer

class TAluniViewSet(viewsets.ModelViewSet):
    queryset = TAluno.objects.all()
    serializer_class = TAlunoSerializer
