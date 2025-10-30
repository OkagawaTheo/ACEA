from django.db import models


class AbstractCurso(models.Model):
    nome = models.CharField(max_length=255,default=''),
    id_curso = models.AutoField(primary_key=True)

    class Meta:
        abstract = True

class Curso(AbstractCurso):
    professores = models.ManyToManyField(
        'pessoa.Professor',
        blank=True,
        related_name='curso_ministrado'
    )

    def __str__(self):
        return self.nome_curso
    


# class AtividadeEsportiva(models.Model):
    