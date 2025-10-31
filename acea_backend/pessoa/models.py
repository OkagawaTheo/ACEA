from django.db import models

class Pessoa(models.Model): # Adicionar OneToOneField com auth.User p/ segurança
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
    # adicionar opcao de criar usuario do admin do sistema também no painel django.

    