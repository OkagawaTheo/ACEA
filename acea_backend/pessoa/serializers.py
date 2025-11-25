from rest_framework import serializers
from .models import Aluno, Professor, Presidente, Administrador, Doador
from curso.models import Curso, AtividadeEsportiva

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = (
            'id_aluno', 'nome', 'cpf', 'tel', 'email', 
            'matricula', 'endereco', 'data_nasc', 
            'cursos_matriculados'
        )
        read_only_fields = ('id_aluno',)
        
class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'
        read_only_fields = ('id_professor',)

class PresidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presidente
        fields = '__all__'
        read_only_fields = ('id_presidente',)

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'
        read_only_fields = ('is_administrador',)

class DoadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doador
        fields = '__all__'
        read_only_fields = ('id_doador',)
        
class MatricularSerializer(serializers.Serializer):
    aluno_id = serializers.IntegerField()
    curso_id = serializers.IntegerField(required=False)
    atividade_id = serializers.IntegerField(required=False)