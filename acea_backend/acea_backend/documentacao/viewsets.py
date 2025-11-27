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
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        
        if (user.is_superuser or 
            hasattr(user, 'presidente') or 
            hasattr(user, 'administrador') or 
            hasattr(user, 'professor')):
            return Pagamento.objects.all()
        
        if hasattr(user, 'aluno'):
            return Pagamento.objects.filter(id_aluno__pk=user.aluno.pk)
            
        return Pagamento.objects.none()

    @action(detail=True, methods=['patch'])
    def gerenciar_pagamento(self, request, pk=None):
        instance = self.get_object()
        serializer = StatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.status = serializer.validated_data['status']
        instance.save()
        return Response(PagamentoSerializer(instance).data, status=status.HTTP_200_OK)

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
    permission_classes = [IsAuthenticated] 
    
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        user = self.request.user
        
        if (user.is_superuser or 
            hasattr(user, 'presidente') or 
            hasattr(user, 'administrador') or 
            hasattr(user, 'professor')):  
            return Documento.objects.all()
            
        return Documento.objects.filter(usuario=user)