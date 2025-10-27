from django.db import models

class Pessoa(models.Model):
    #nome cpf tel email
    nome = models.CharField(max_length=100)
    cpf = models.
