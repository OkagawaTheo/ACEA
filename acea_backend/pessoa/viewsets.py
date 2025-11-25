from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Aluno, Professor, Presidente, Administrador, Doador
from .serializers import AlunoSerializer, ProfessorSerializer, PresidenteSerializer, AdministradorSerializer, DoadorSerializer, MatricularSerializer
from curso.models import Curso, AtividadeEsportiva
from .permissions import IsPresidenteOrAdmin, IsProfessor


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsPresidenteOrAdmin | IsAuthenticated]

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsPresidenteOrAdmin | IsProfessor]

    @action(detail=False, methods=['post'])
    def matricular_aluno(self, request):
        serializer = MatricularSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        aluno = get_object_or_404(Aluno, pk=serializer.validated_data['aluno_id'])
        
        if serializer.validated_data.get('curso_id'):
            curso = get_object_or_404(Curso, pk=serializer.validated_data['curso_id'])
            aluno.cursos_matriculados.add(curso)

        if serializer.validated_data.get('atividade_id'):
            atividade = get_object_or_404(AtividadeEsportiva, pk=serializer.validated_data['atividade_id'])
            aluno.cursos_matriculados.add(atividade)

        aluno.save()
        return Response(AlunoSerializer(aluno).data, status=status.HTTP_200_OK)

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
    permission_classes = [IsPresidenteOrAdmin | IsAuthenticated]