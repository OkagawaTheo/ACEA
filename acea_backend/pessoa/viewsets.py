from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser 
from .permissions import IsPresidenteOrAdmin, IsProfessor 
from .models import Aluno, Professor, Presidente, Administrador, Doador
from .serializers import AlunoSerializer, ProfessorSerializer, PresidenteSerializer, AdministradorSerializer, DoadorSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsPresidenteOrAdmin | IsAuthenticatedOrReadOnly] 

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsPresidenteOrAdmin | IsProfessor]

class PresidenteViewSet(viewsets.ModelViewSet):
    queryset = Presidente.objects.all()
    serializer_class = PresidenteSerializer
    permission_classes = [IsAdminUser]

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [IsAdminUser]

class DoadorViewSet(viewsets.ModelViewSet):
    queryset = Doador.objects.all()
    serializer_class = DoadorSerializer
    permission_classes = [IsPresidenteOrAdmin | IsAuthenticatedOrReadOnly]