from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14,unique=True)
    phone = models.CharField(max_length=14,blank=True)
    email = models.EmailField(max_length=255)

    class Meta:
        abstract = True



class TAluno(Pessoa):
    # adicionar relacionamentos N:N(1)
    dataNascimento = models.DateField(null=True,blank=True)
    endereco = models.CharField(max_length=255)
    
    def criarAluno(self):
        pass

    def editarAluno(self):
        pass

    def excluirAluno(self):
        pass

    def visualizarAluno(self):
        pass

    def __str__(self):
        return f"Aluno: {self.nome}"

class TProfessor(Pessoa):
    especialidade = models.CharField(max_length=100)

    def cadastrarAluno(): #TAluno<curso>: Tcurso,atividade>, TAtividadeEspo.
        pass

    def visualizarPagamentos(): #list<TPagamentos>
        pass

    def gerenciarCurso():
        pass

    def gerenciarAtividadeEsportiva():
        pass

    def criarProfessor():
        pass

    def alterarProfessor():
        pass

    def excluirProfessor():
        pass

    def visualizarProfessor():
        pass

    