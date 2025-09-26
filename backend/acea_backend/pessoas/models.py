from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=14, blank=True, null=True)
    email = models.EmailField(max_length=255)

    class Meta:
        abstract = True
        
    def __str__(self):
        return self.nome


class TAluno(Pessoa):
    # add CRUD em services depois de construir a logica
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=255)
    
    cursos = models.ManyToManyField('educacao.TCurso', related_name='alunos')
    atividades = models.ManyToManyField('educacao.TAtividade_esportiva',related_name='alunos_atividades')

    def criar_aluno(self):
        pass

    def editar_aluno(self):
        pass

    def excluir_aluno(self):
        pass

    def visualizar_aluno(self):
        pass

    def __str__(self):
        return f"Aluno: {self.nome}"


class TProfessor(Pessoa):
    especialidade = models.CharField(max_length=100)

    def cadastrar_aluno(self):
        pass

    def visualizar_pagamentos(self):
        pass

    def gerenciar_curso(self):
        pass

    def gerenciar_atividade_esportiva(self):
        pass

    def criar_professor(self):
        pass

    def alterar_professor(self):
        pass

    def excluir_professor(self):
        pass

    def visualizar_professor(self):
        pass

    def __str__(self):
        return f"Professor: {self.nome}"


class TPresidente(Pessoa):
    
    def visualizar_pagamento(self):
        pass
        
    def gerenciar_doacoes(self):
        pass
        
    def controlar_documento(self):
        pass
        
    def download_documento(self):
        pass

    def criar_presidente(self):
        pass
        
    def alterar_presidente(self):
        pass
        
    def excluir_presidente(self):
        pass
        
    def __str__(self):
        return f"Presidente: {self.nome}"


class TAdm(Pessoa):
    
    def gerenciar_professor(self):
        pass

    def gerenciar_presidente(self):
        pass
        
    def __str__(self):
        return f"Administrador: {self.nome}"