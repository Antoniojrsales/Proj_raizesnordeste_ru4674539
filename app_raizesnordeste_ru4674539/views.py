from rest_framework import generics
from .domain.produto import Produto
from .domain.pedido import Pedido
from .application.serializers import ProdutoSerializer, PedidoSerializer

class ProdutoListAPIView(generics.ListAPIView):
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        """
        Filtro dinâmico por filial via URL para o RF05 (Regionalização).
        """
        queryset = Produto.objects.filter(disponivel=True)
        filial_id = self.request.query_params.get('filial')
        
        if filial_id is not None:
            queryset = queryset.filter(filiais__id_filial=filial_id)
            
        return queryset


class PedidoListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint para o Totem/App registrarem um novo pedido (POST).
    Processa os itens, calcula o valor total e dispara os pontos de fidelidade (RF03).
    """
    queryset = Pedido.objects.all().order_by('-data_pedido')
    serializer_class = PedidoSerializer