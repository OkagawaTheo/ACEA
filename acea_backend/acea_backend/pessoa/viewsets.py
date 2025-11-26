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
from django.db.models import Q
from rest_framework.permissions import AllowAny

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    
    def get_permissions(self):
        # 1. Aluno vê o próprio perfil
        if self.action == 'meus_dados':
            return [IsAuthenticated()]
        
        # 2. Admin e Professor podem ver a LISTA de alunos e DETALHES
        # 'list' = ver todos / 'retrieve' = ver um específico
        elif self.action in ['list', 'retrieve']:
            return [(IsPresidenteOrAdmin | IsProfessor)()] # CORRETO

        # 3. Criar, Editar ou Deletar alunos -> SÓ ADMIN/PRESIDENTE
        else:
            return [IsPresidenteOrAdmin()]

    # 3. A AÇÃO SEGURA (Que o Aluno pode acessar)
    @action(detail=False, methods=['get'])
    def meus_dados(self, request):
        usuario = request.user
        try:
            # Pega apenas o aluno ligado a este usuário
            aluno = usuario.aluno 
            serializer = self.get_serializer(aluno)
            return Response(serializer.data)
        except Exception:
            return Response({"erro": "Perfil não encontrado"}, status=404)
    
class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    
    def get_permissions(self):
        # Liberamos 'meus_dados' (perfil) e 'meus_alunos' (lista) para o professor logado
        if self.action in ['meus_dados', 'meus_alunos', 'matricular_aluno']:
            return [IsAuthenticated()]
        # O resto (criar/deletar professor) só Admin
        return [IsPresidenteOrAdmin()]

    # --- AÇÃO DE PERFIL DO PROFESSOR (NOVA) ---
    @action(detail=False, methods=['get'])
    def meus_dados(self, request):
        usuario = request.user
        try:
            # Tenta pegar o perfil de professor ligado a este usuário
            # (Isso funciona graças ao related_name='professor' no models.py)
            prof = usuario.professor
            serializer = self.get_serializer(prof)
            return Response(serializer.data)
        except Exception:
            return Response({"erro": "Perfil de professor não encontrado."}, status=404)

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

    # Mudei de detail=True para False
    @action(detail=False, methods=['get'])
    def meus_alunos(self, request):
        # Em vez de pegar pelo ID da URL, pegamos pelo Token (mais seguro)
        professor = request.user.professor 
        
        # Filtra alunos vinculados a este professor
        alunos_cursos = Aluno.objects.filter(cursos_matriculados__professores=professor)
        alunos_atividades = Aluno.objects.filter(cursos_matriculados__atividadeesportiva__id_professor=professor)
        
        alunos = (alunos_cursos | alunos_atividades).distinct()
        
        serializer = AlunoSerializer(alunos, many=True)
        return Response(serializer.data)

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