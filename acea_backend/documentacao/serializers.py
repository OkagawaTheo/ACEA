from rest_framework import serializers
from .models import Pagamento, Doacao

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