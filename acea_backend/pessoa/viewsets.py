from rest_framework import viewsets
from .models import Aluno, Professor, Presidente, Administrador, Doador
from .serializers import AlunoSerializer, ProfessorSerializer, PresidenteSerializer, AdministradorSerializer, DoadorSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class PresidenteViewSet(viewsets.ModelViewSet):
    queryset = Presidente.objects.all()
    serializer_class = PresidenteSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer

class DoadorViewSet(viewsets.ModelViewSet):
    queryset = Doador.objects.all()
    serializer_class = DoadorSerializer