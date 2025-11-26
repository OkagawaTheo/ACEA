from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated # <--- Importante
from pessoa.permissions import IsPresidenteOrAdmin, IsOwnerOrAdmin
from .models import Pagamento, Doacao
from .serializers import PagamentoSerializer, DoacaoSerializer, StatusUpdateSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Pagamento, Doacao, Documento
from .serializers import PagamentoSerializer, DoacaoSerializer, DocumentoSerializer

class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    # Permitimos Autenticados gerais (o filtro real acontece no get_queryset)
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        
        # 1. Admin, Presidente E PROFESSOR veem tudo
        if (user.is_superuser or 
            hasattr(user, 'presidente') or 
            hasattr(user, 'administrador') or 
            hasattr(user, 'professor')): # <--- ADICIONADO PROFESSOR AQUI
            return Pagamento.objects.all()
        
        # 2. Aluno vê apenas os seus
        if hasattr(user, 'aluno'):
            return Pagamento.objects.filter(id_aluno__pk=user.aluno.pk)
            
        return Pagamento.objects.none()

    # (Mantenha o método gerenciar_pagamento igual estava...)
    @action(detail=True, methods=['patch'])
    def gerenciar_pagamento(self, request, pk=None):
        # ... (seu código antigo) ...
        instance = self.get_object()
        serializer = StatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.status = serializer.validated_data['status']
        instance.save()
        return Response(PagamentoSerializer(instance).data, status=status.HTTP_200_OK)

# (Mantenha DoacaoViewSet igual...)
class DoacaoViewSet(viewsets.ModelViewSet):
    queryset = Doacao.objects.all()
    serializer_class = DoacaoSerializer
    permission_classes = [IsPresidenteOrAdmin]
    
    @action(detail=False, methods=['post'])
    def registrar_doacao(self, request):
        doacao_serializer = DoacaoSerializer(data=request.data)
        doacao_serializer.is_valid(raise_exception=True)
        doacao = doacao_serializer.save(id_adm=request.user.administrador if hasattr(request.user, 'administrador') else None)
        return Response(DoacaoSerializer(doacao).data, status=status.HTTP_201_CREATED)

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated] # Só quem tem Token entra
    
    # Habilita o Django a receber arquivos
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        user = self.request.user
        
        # AGORA: Professor também entra no grupo que vê tudo (all)
        if (user.is_superuser or 
            hasattr(user, 'presidente') or 
            hasattr(user, 'administrador') or 
            hasattr(user, 'professor')):  # <--- ADICIONADO
            return Documento.objects.all()
            
        # Aluno continua vendo só os dele
        return Documento.objects.filter(usuario=user)