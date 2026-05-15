from django.urls import path
from .views import ProdutoListAPIView

urlpatterns = [
    path('produtos/', ProdutoListAPIView.as_view(), name='produto-list'),
]