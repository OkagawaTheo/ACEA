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
        related_name='curso_ministrado',
        
    )    
    # add horários pra selecionar/visualizar
    # add choices p/ cursos
    

class AtividadeEsportiva(AbstractCurso):
    id_ativesportiva = models.AutoField(primary_key=True)

    id_professor = models.ForeignKey(
        Professor,
        default='',   
        on_delete=models.SET_DEFAULT,
        related_name='atividade_ministrado',
    )
    
class Horario(models.Model):
    DIA_SEMANA = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira'),
        ('SAB', 'Sábado'),
    ]

    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=3, choices=DIA_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f"{self.get_dia_display()} - {self.hora_inicio}"