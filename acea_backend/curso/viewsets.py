from rest_framework import viewsets
from .models import Curso, AtividadeEsportiva
from .serializers import CursoSerializer, AtividadeEsportivaSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class AtividadeEsportivaViewSet(viewsets.ModelViewSet):
    queryset = AtividadeEsportiva.objects.all()
    serializer_class = AtividadeEsportivaSerializer