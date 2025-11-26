
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentacao', '0004_pagamento_status_alter_pagamento_id_adm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='status',
            field=models.CharField(choices=[('PG', 'Pago'), ('NP', 'Não Pago')], default='NP', max_length=3, verbose_name='Status de Pagamento:'),
        ),
    ]
