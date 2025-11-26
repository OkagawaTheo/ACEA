from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Pessoa(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) 
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11,unique=True,db_column="CPF")
    tel = models.CharField(max_length=14,blank=True,null=True) 
    email = models.EmailField(max_length=50,unique=True,default='') 
    
    class Meta:
        abstract = True
    def __str__(self):
        return self.nome
    
class Aluno(Pessoa): 
    id_aluno = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=50,default='',unique=True)
    endereco = models.CharField(max_length=255,blank=True,null=True)
    data_nasc = models.DateTimeField(default= timezone.now)
    cursos_matriculados = models.ManyToManyField( 
        'curso.Curso',
        blank = True,
        related_name='alunos_matriculados'
    )


class Professor(Pessoa):
    id_professor = models.AutoField(primary_key=True)
    especialidade = models.CharField(max_length=100)


class Presidente(Pessoa): 
    id_presidente = models.AutoField(primary_key=True)
    is_superuser = models.BooleanField(default=True,verbose_name="Presidente")
    

class Administrador(Pessoa):
    tel = None
    is_administrador = models.AutoField(primary_key=True)
    is_superuser = models.BooleanField(default=True,verbose_name="Administrador")

class Doador(Pessoa):
    id_doador = models.AutoField(primary_key=True)