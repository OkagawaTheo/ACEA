from rest_framework import serializers
from .models import *

class TAlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TAluno
        fields = ('id', 'nome', 'cpf', 'telefone', 'email', 'data_nascimento', 'endereco', 'cursos', 'atividades')

class TProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TProfessor
        fields = ('id','nome','cpf','telefone','email','especialidade','cursos_ministrados','atividades_ministradas')

class TPresidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPresidente
        fields = ('id','nome','cpf','telefone','email')

        
class TAdmSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPresidente
        fields= ('id','nome','cpf','telefone','email')

