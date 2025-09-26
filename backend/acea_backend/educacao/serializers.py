from rest_framework import serializers
from .models import *

class TCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TCurso
        fields = ('id','nome','descricao','horario','valor_mensalidade','professor','alunos')

class TAtividade_esportivaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TAtividade_esportiva
        fields = ('id','nome','descricao','horario','valor_mensalidade')



        