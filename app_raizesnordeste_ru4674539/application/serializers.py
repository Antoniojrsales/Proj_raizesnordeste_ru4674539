from rest_framework import serializers
from django.db import transaction
from ..domain.filial import Filial
from ..domain.produto import Produto, CategoriaProduto
from ..domain.pedido import Pedido, ItensPedido
from ..domain.cliente import Cliente

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

class ItensPedidoSerializer(serializers.ModelSerializer):
    # Mantemos para a escrita reconhecer o ID do produto vindo do Totem
    id_produto = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all())
    # Adicionamos esses campos como ReadOnly para o GET trazer os detalhes mastigados
    nome_produto = serializers.ReadOnlyField(source='id_produto.nome_produto')
    preco_pago = serializers.DecimalField(max_digits=10, decimal_places=2, source='preco_unitario', read_only=True)

    class Meta:
        model = ItensPedido
        fields = ['id_produto', 'nome_produto', 'quantidade', 'preco_pago']


class PedidoSerializer(serializers.ModelSerializer):
    # Criamos um campo dinâmico que vai buscar os itens diretamente no banco de dados
    itens = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ['id_pedido', 'id_cliente', 'id_filial', 'canal_venda', 'itens', 'valor_total', 'data_pedido']
        read_only_fields = ['id_pedido', 'valor_total', 'data_pedido']

    def get_itens(self, obj):
        """
        Este método busca ativamente todos os itens associados a este pedido
        e os formata usando o ItensPedidoSerializer.
        """
        from ..domain.pedido import ItensPedido  # Ajuste o import se necessário para o seu arquivo
        # Buscamos os itens que apontam para o ID deste pedido
        itens_do_pedido = ItensPedido.objects.filter(id_pedido=obj)
        return ItensPedidoSerializer(itens_do_pedido, many=True).data

    def create(self, validated_data):
        # Para a escrita (POST), pescamos a lista de itens bruta do JSON enviado
        # O DRF guarda os dados que não são mapeados diretamente no dict inicial
        itens_data = self.initial_data.get('itens', [])
        
        with transaction.atomic():
            pedido = Pedido.objects.create(valor_total=0, **validated_data)
            valor_total_pedido = 0
            
            for item_data in itens_data:
                from ..domain.produto import Produto  # Ajuste o import se necessário
                from ..domain.pedido import ItensPedido

                produto = Produto.objects.get(pk=item_data['id_produto'])
                quantidade = int(item_data['quantidade'])
                
                preco_unitario = produto.preco_unitario
                valor_total_pedido += preco_unitario * quantidade
                
                ItensPedido.objects.create(
                    id_pedido=pedido,
                    id_produto=produto,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario
                )
            
            pedido.valor_total = valor_total_pedido
            pedido.save()
            
            # Gatilho de fidelidade (RF03)
            cliente = pedido.id_cliente
            if cliente:
                pontos_gerados = int(valor_total_pedido)
                cliente.saldo_pontos += pontos_gerados
                cliente.save()
                
            return pedido