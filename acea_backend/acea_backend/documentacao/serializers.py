from rest_framework import serializers
from .models import Pagamento, Doacao, Documento

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'
        read_only_fields = ('id_pagamento',)

class DoacaoSerializer(serializers.ModelSerializer):
    doador_nome = serializers.ReadOnlyField(source='id_doador.nome')

    class Meta:
        model = Doacao
        fields = '__all__'
        read_only_fields = ('id_doacao',)

class StatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Pagamento.statusPagamento.choices)

class DocumentoSerializer(serializers.ModelSerializer):
    nome_usuario = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Documento
        fields = '__all__'
        read_only_fields = ('id_documento', 'usuario', 'data_envio')
