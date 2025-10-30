from django.db import models
from pessoa.models import Professor

<<<<<<< HEAD
class AbstractCurso(models.Model):
    nome = models.CharField(max_length=255,default='')

    class Meta:
        abstract = True
    def __str__(self):
        return self.nome

class Curso(AbstractCurso):
    id_curso = models.AutoField(primary_key=True)

    professores = models.ManyToManyField(
=======
class abstractCurso(models.Model):
    nome = models.CharField(max_length=255,default='',)

    class Meta:
        abstract = True

    def __str__(self):
        return abstractCurso.nome

class Curso(abstractCurso):
    id_curso = models.AutoField(primary_key=True)
    nome_curso = models.CharField(max_length=255,default='')
    
    professores_curso = models.ManyToManyField(
>>>>>>> a66c41c (Model de AtividadeEsportiva implementada)
        'pessoa.Professor',
        blank=True,
        related_name='curso_ministrado',
    )    

<<<<<<< HEAD
    class Meta:
        db_table = 'Curso'

class AtividadeEsportiva(AbstractCurso):
    id_ativesportiva = models.AutoField(primary_key=True)

    id_professor = models.ForeignKey(
        Professor,
        blank=True,
        default='',   
    )
    
=======
    def __str__(self):
        return self.nome_curso
    
class AtividadeEsportiva(abstractCurso):
    id_atvesportiva = models.AutoField(primary_key=True)

    id_professor = models.ForeignKey(
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='ativesportiva_ministrado'
        )
    
>>>>>>> a66c41c (Model de AtividadeEsportiva implementada)
