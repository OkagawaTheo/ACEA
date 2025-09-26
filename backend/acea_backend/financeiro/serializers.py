from rest_framework import serializers
from .models import *

class TPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPagamento
        fields = ('id', 'valor', 'data', 'tipo', 'status', 'aluno')

class TDoacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TDoacao
        fields = ('id', 'valor', 'data', 'doador_info')

class TDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TDocumento
        fields = ('id', 'nome', 'tipo', 'data_upload', 'arquivo')
        