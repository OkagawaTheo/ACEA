from django.db import models
from pessoa.models import Professor

class AbstractCurso(models.Model):
    nome = models.CharField(max_length=255,default='')

    class Meta:
        abstract = True
    def __str__(self):
        return self.nome

class Curso(AbstractCurso):
    id_curso = models.AutoField(primary_key=True)

    professores = models.ManyToManyField(
        'pessoa.Professor',
        blank=True,
        related_name='curso_ministrado',
    )    

    class Meta:
        db_table = 'Curso'

class AtividadeEsportiva(AbstractCurso):
    id_ativesportiva = models.AutoField(primary_key=True)

    id_professor = models.ForeignKey(
        Professor,
        blank=True,
        default='',   
    )
    
