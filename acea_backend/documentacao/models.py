from django.db import models

class Pagamento(models.Model):
    class TipoPagamento(models.TextChoices):
        MENSALIDADE = 'MEN', 'Mensalidade',
        DOACAO = 'DOA', 'Doação',
        EVENTO = 'EVE', 'Evento',
        OUTRO = 'OUT', 'Outro'

    id_pagamento = models.AutoField(unique=True,primary_key=True)
    valor = models.DecimalField(decimal_places=2,max_digits=10)
    data_pagamento = models.DateField(auto_now=True)

    tipo_pagamento = models.CharField(
        max_length=3,
        choices=TipoPagamento.choices,
        default=TipoPagamento.MENSALIDADE,
        verbose_name="Tipo de Pagamento"
    )

    id_adm = models.ForeignKey(
        'pessoa.Administrador',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pagamentos_gerenciados',
        verbose_name="Administrador"
    )
    def __str__(self):
        return f"{self.get_tipo_pagamento_display()} - R$ {self.valor}"



