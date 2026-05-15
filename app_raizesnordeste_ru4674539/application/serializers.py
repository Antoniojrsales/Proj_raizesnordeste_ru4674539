from rest_framework import serializers
from ..domain.filial import Filial
from ..domain.produto import Produto, CategoriaProduto

class FilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = '__all__'

class CategoriaProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProduto
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    # Mostra o nome da categoria em vez de apenas o ID
    categoria_nome = serializers.ReadOnlyField(source='id_categoria.nome_categoria')
    
    class Meta:
        model = Produto
        fields = [
            'id_produto', 'nome_produto', 'preco_unitario', 
            'unidade_medida', 'is_sazonal', 'disponivel', 
            'categoria_nome', 'filiais'
        ]