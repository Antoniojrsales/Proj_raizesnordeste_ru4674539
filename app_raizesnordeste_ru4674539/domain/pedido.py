from django.db import models
from .cliente import Cliente
from .filial import Filial
from .produto import Produto
from .canal_venda import CanalVenda

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('RECUSADO', 'Recusado'),
    ]

    id_pedido = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    canal_venda = models.CharField(max_length=20)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_pedido = models.DateTimeField(auto_now_add=True)
    
    # Nosso novo campo para o RF02
    status_pagamento = models.CharField(max_length=15, 
                                        choices=STATUS_CHOICES, 
                                        default='PENDENTE')

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.status_pagamento}"

class ItensPedido(models.Model):
    id_item_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    id_produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Preço no momento da venda

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade}x {self.id_produto.nome_produto}"