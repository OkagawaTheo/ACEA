from rest_framework import serializers
from django.contrib.auth.models import User # Importante para criar o login
from .models import Aluno, Professor, Presidente, Administrador, Doador, Pessoa
from curso.models import Curso, AtividadeEsportiva
from django.db import IntegrityError

# --- Lógica Automática de Criação de Usuário ---
def criar_usuario_automatico(dados, tipo):
    """
    Cria um User do Django automaticamente.
    - Username: O CPF (para garantir unicidade)
    - Senha Padrão: O CPF (o aluno pode mudar depois)
    """
    cpf = dados.get('cpf')
    email = dados.get('email')
    
    if not cpf:
        raise serializers.ValidationError({"erro": "CPF é obrigatório para gerar o login."})

    # Cria o usuário no sistema de autenticação
    user = User.objects.create_user(
        username=cpf,  # O Login será o CPF
        email=email,
        password=cpf   # A Senha inicial será o CPF
    )
    return user

# -----------------------------------------------

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'
        read_only_fields = ('id_aluno', 'user')

    def create(self, validated_data):
        cursos_data = validated_data.pop('cursos_matriculados', [])

        try:
            # Tenta criar o usuário
            user = criar_usuario_automatico(validated_data, 'aluno')
        except IntegrityError:
            # Se o banco reclamar que já existe, devolve erro amigável (400)
            raise serializers.ValidationError({"erro": "Este CPF já possui um cadastro de usuário no sistema."})
        except Exception as e:
            raise serializers.ValidationError({"erro": str(e)})
        
        # Cria o aluno
        aluno = Aluno.objects.create(user=user, **validated_data)
        
        # Vincula cursos
        if cursos_data:
            aluno.cursos_matriculados.set(cursos_data)
        
        return aluno

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'
        read_only_fields = ('id_professor', 'user')

    def create(self, validated_data):
        # 1. Cria o Login (User)
        user = criar_usuario_automatico(validated_data, 'professor')
        
        # 2. Cria o Professor vinculado a esse User
        professor = Professor.objects.create(user=user, **validated_data)
        return professor

# --- Outros Serializers (Não precisam mudar agora) ---
class PresidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presidente
        fields = '__all__'

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'

class DoadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doador
        fields = '__all__'

class MatricularSerializer(serializers.Serializer):
    aluno_id = serializers.IntegerField()
    curso_id = serializers.IntegerField(required=False)
    atividade_id = serializers.IntegerField(required=False)