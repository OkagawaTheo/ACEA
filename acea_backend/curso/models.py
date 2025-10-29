from django.db import models
from pessoa.models import Professor

class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nome_curso = models.CharField(max_length=255,default='')
    
    professores = models.ManyToManyField(
        Professor,
        blank=True,
        related_name='curso_ministrado'
    )

    def __str__(self):
        return self.nome_curso