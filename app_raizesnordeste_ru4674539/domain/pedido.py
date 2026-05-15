from django.db import models
from .cliente import Cliente
from .filial import Filial
from .produto import Produto

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    # Relacionamentos
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    
    data_pedido = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pontos_gerados = models.IntegerField(default=0)
    
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Preparando', 'Preparando'),
        ('Concluido', 'Concluído'),
        ('Cancelado', 'Cancelado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    
    # Canal de venda (Totem, App, Balcão)
    canal_venda = models.CharField(max_length=50) 

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.id_cliente.nome_completo}"

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