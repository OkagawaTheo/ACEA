from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from pessoa.permissions import IsPresidenteOrAdmin
from .models import Curso, AtividadeEsportiva
from .serializers import CursoSerializer, AtividadeEsportivaSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'meus_cursos', 'meus_cronogramas']: 
            return [IsAuthenticated()]
        else:
            return [IsPresidenteOrAdmin()]

    @action(detail=False, methods=['get'])
    def meus_cursos(self, request):
        user = request.user
        if hasattr(user, 'aluno'):
            cursos = Curso.objects.filter(alunos_matriculados=user.aluno)
            serializer = self.get_serializer(cursos, many=True)
            return Response(serializer.data)
        return Response([])

    @action(detail=False, methods=['get'])
    def meus_cronogramas(self, request):
        user = request.user
        if hasattr(user, 'professor'):
            meus_cursos = Curso.objects.filter(professores=user.professor)
            serializer = self.get_serializer(meus_cursos, many=True)
            return Response(serializer.data)
        return Response({"aviso": "Você não é professor."}, status=403)

class AtividadeEsportivaViewSet(viewsets.ModelViewSet):
    queryset = AtividadeEsportiva.objects.all()
    serializer_class = AtividadeEsportivaSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'minhas_atividades']:
            return [IsAuthenticated()]
        else:
            return [IsPresidenteOrAdmin()]

    @action(detail=False, methods=['get'])
    def minhas_atividades(self, request):
        user = request.user
        if hasattr(user, 'aluno'):
            atividades = AtividadeEsportiva.objects.filter(alunos_inscritos=user.aluno)
            return Response(self.get_serializer(atividades, many=True).data)
        return Response([])