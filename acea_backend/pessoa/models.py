from django.db import models

class Pessoa(models.Model):
    #nome cpf tel email
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14,unique=True)
    tel = models.CharField(max_length=15,blank=True,null=True) 
    email = models.EmailField(unique=True)

    class Meta:
        abstract = True;

    def __str__(self):
        return self.nome
    
class Aluno(Pessoa):
    data_nasc = models.DateField()
    endereco = models.CharField(max_length=400)

    # relations

class Professor(Pessoa):
    especialidade = models.CharField(max_length=100) # add choices depois (puxar do banco)


class Presidente(Pessoa):
    pass