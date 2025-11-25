from django.db import models
from django.utils import timezone
from decimal import Decimal

class Pagamento(models.Model):
    class TipoPagamento(models.TextChoices):
        MENSALIDADE = 'MEN', 'Mensalidade',
        DOACAO = 'DOA', 'Doação',
        EVENTO = 'EVE', 'Evento',
        OUTRO = 'OUT', 'Outro'

    class statusPagamento(models.TextChoices):
        PAGO = 'PG', 'Pago'
        NAO_PAGO = 'NP', 'Não Pago',
    

    id_pagamento = models.AutoField(unique=True,primary_key=True)
    valor = models.DecimalField(decimal_places=2,max_digits=10,default=Decimal('0.00'))
    data_pagamento = models.DateField(default=timezone.now)

    tipo_pagamento = models.CharField(
        max_length=3,
        choices=TipoPagamento.choices,
        default=TipoPagamento.MENSALIDADE,
        verbose_name="Tipo de Pagamento",
    )

    status = models.CharField(
        max_length=3,
        choices=statusPagamento.choices,
        default="NP",
        verbose_name='Status de Pagamento:'
    )

    id_adm = models.ForeignKey(
        'pessoa.Administrador',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pagamentos_gerenciados',
        verbose_name="Administrador"
    )

    id_aluno = models.ForeignKey(
        'pessoa.Aluno',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='aluno_pagante',
        verbose_name='Aluno'
    )
    def __str__(self):
        return f"{self.get_tipo_pagamento_display()} - R$ {self.valor}"


class Doacao(models.Model):
    id_doacao = models.AutoField(primary_key=True)
    id_doador = models.ForeignKey(
        'pessoa.Doador',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Doador',
        related_name="doacoes_feitas"

    )
    valor = models.DecimalField(decimal_places=2,max_digits=10,default=Decimal('0.00'))
    data_doacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Doação de R$ {self.valor} | {self.id_doador}"

