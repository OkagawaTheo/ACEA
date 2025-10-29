from django.db import models

class Pessoa(models.Model):
    #nome cpf tel
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11,unique=True,db_column="CPF")
    tel = models.CharField(max_length=14,blank=True,null=True) 
    email = models.EmailField(max_length=50,unique=True) 
    
    class Meta:
        abstract = True;

    def __str__(self):
        return self.nome
    
class Aluno(Pessoa):
    id_aluno = models.IntegerField(primary_key=True,default=0)
    matricula = models.CharField(max_length=50,default='')
    curso = models.CharField(max_length=100,default='')
    endereco = models.CharField(max_length=255,blank=True,null=True)

    #<pk<id>>

    # relations mtm mt1

class Professor(Pessoa):
    id_profesor = models.IntegerField(primary_key=True) #FK com documento  
    especialidade = models.CharField(max_length=100)


class Presidente(Pessoa):
    id_presidente 
    

# adm é BOOLEAN