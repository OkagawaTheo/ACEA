from django.db import models

class TPagamento(models.Model):
    valor = models.DecimalField(max_digits=10,decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=50) 
    status = models.CharField(max_length=50) 

    aluno = models.ForeignKey(
        'pessoas.TAluno',
        on_delete=models.CASCADE,
        related_name= 'pagamentos'
    )

    def criar_pagamento(self):
        pass

    def editar_pagamento(self):
        pass

    def visualizar_pagamento(self):
        pass

    def excluir_pagamento(self):
        pass

    def __str__(self):
        return f"Pagamento R$ {self.valor}"
    
class TDoacao(models.Model):
    valor = models.DecimalField(max_digits=10,decimal_places=2)
    data = models.DateField()
    doador_info = models.CharField(max_length=255)

    def criar_doacao(self):
        pass

    def excluir_doacao(self):
        pass

    def visualizar_doacao(self):
        pass

    def __str__(self):
        return f"Doação R$ {self.valor} de {self.doador_info}"
    

class TDocumentos(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50)
    data_upload = models.DateTimeField(auto_now_add=True)

    arquivo = models.FileField(upload_to='Documentos/', null=True,blank=True) # Alterar depois o local de upload de arquivo

    def criar_documento(self):
        pass

    def excluir_documento(self):
        pass

    def editar_documento(self):
        pass

    def visualizar_documento(self):
        pass

    def __str__(self):
        return self.nome
    
