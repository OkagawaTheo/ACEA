from rest_framework import serializers
from .models import Curso, AtividadeEsportiva, Horario

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ['id', 'dia', 'hora_inicio', 'hora_fim'] # Usei lista explicita para ficar claro

class CursoSerializer(serializers.ModelSerializer):
    horarios = HorarioSerializer(many=True, read_only=True)

    class Meta:
        model = Curso
        fields = '__all__'
        read_only_fields = ('id_curso',)

class AtividadeEsportivaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtividadeEsportiva
        fields = '__all__'
        read_only_fields = ('id_ativesportiva',)