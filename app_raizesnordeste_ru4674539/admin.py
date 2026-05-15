from django.contrib import admin
from .domain import Cliente, Filial, CanalVenda, Produto, CategoriaProduto, Pedido, ItensPedido

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'email', 'saldo_pontos')
    search_fields = ('nome_completo', 'cpf')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome_produto', 'preco_unitario', 'disponivel')
    list_filter = ('id_categoria', 'is_sazonal')

# Registros simples para os demais
admin.site.register(Filial)
admin.site.register(CanalVenda)
admin.site.register(CategoriaProduto)
admin.site.register(Pedido)
admin.site.register(ItensPedido)