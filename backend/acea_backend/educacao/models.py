from django.db import models


class Educacao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True,null=True)
    horario = models.CharField(max_length=50)
    valor_mensalidade = models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        abstract = True


    def __str__(self):
        return self.nome

class TCurso(Educacao):

    #Relacionamento
    professor = models.ForeignKey(
        'pessoas.TProfessor',
        on_delete=models.SET_NULL,
        null=True,
        related_name='cursos_ministrados' 
    )

    def criar_curso(self):
        pass
        
    def editar_curso(self):
        pass
        
    def visualizar_curso(self):
        pass
        
    def adicionar_aluno(self):
        pass


class TAtividade_esportiva(Educacao):
    def criar_atividade_esportiva(self):
        pass

    professor = models.ForeignKey(
        'pessoas.TProfessor',
        on_delete=models.SET_NULL,
        null = True,
        related_name='atividades_ministradas'
    )

    def criar_atividade_esportiva(self):
        pass
        
    def visualizar_atividade_esportiva(self):
        pass

    def editar_atividade_esportiva(self):
        pass

    def adicionar_aluno(self):
        pass

