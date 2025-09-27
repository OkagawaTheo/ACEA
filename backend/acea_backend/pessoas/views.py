from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny

class TAlunoViewSet(viewsets.ModelViewSet):
    queryset = TAluno.objects.all()
    serializer_class = TAlunoSerializer
    permission_classes = [AllowAny]

class TProfessorViewSet(viewsets.ModelViewSet):
    queryset = TProfessor.objects.all()
    serializer_class = TProfessorSerializer
    permission_classes = [AllowAny]


class TPresidenteViewSet(viewsets.ModelViewSet):
    queryset = TPresidente.objects.all()
    serializer_class = TPresidenteSerializer
    permission_classes = [AllowAny]

class TAdmViewSets(viewsets.ModelViewSet):
    queryset = TAdm.objects.all()
    serializer_class = TAdmSerializer
    permission_classes = [AllowAny]

