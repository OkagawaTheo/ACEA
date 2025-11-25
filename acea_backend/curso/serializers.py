from rest_framework import serializers
from .models import Curso, AtividadeEsportiva

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'
        read_only_fields = ('id_curso',)

class AtividadeEsportivaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtividadeEsportiva
        fields = '__all__'
        read_only_fields = ('id_ativesportiva',)