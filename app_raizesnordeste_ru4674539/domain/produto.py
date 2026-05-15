from django.db import models
from .filial import Filial

class CategoriaProduto(models.Model):
    id_categoria_produto = models.AutoField(primary_key=True)
    nome_categoria = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome_categoria

class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    filiais = models.ManyToManyField(Filial, related_name='produtos')
    id_categoria = models.ForeignKey(CategoriaProduto, on_delete=models.PROTECT)
    
    nome_produto = models.CharField(max_length=100)
    fornecedor = models.CharField(max_length=100, null=True, blank=True)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    validade_produto = models.DateField(null=True, blank=True)
    unidade_medida = models.CharField(max_length=20)
    
    is_sazonal = models.BooleanField(default=False) # Atende RF05
    disponivel = models.BooleanField(default=True)  # Controle de estoque/visibilidade

    def __str__(self):
        return self.nome_produto
    