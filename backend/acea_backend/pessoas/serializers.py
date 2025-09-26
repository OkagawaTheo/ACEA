from rest_framework import serializers
from .models import TAluno

class TAlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TAluno
        fields = ('id', 'nome', 'cpf', 'telefone', 'email', 'data_nascimento', 'endereco', 'cursos', 'atividades')
