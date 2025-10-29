from django.db import models

class Pagamento(models.Model):
    id_pagamento = models.AutoField(unique=True,primary_key=True)
    valor = models.DecimalField(decimal_places=2,max_digits=10)
    data_pagamento = models.DateField(auto_now=True)
    #tipo_pagamento 
    



#Required loginMixIn index

