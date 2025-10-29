from django.db import models

class Pagamento(models.Model):
    id_pagamento = models.IntegerField(unique=True,primary_key=True)
    valor = models.DecimalField(decimal_places=2)
    data = models.DateField(auto_now=True)
    
#Required loginMixIn index

