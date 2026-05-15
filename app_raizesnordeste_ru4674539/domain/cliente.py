from django.db import models

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome_completo = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True) # Unique para evitar duplicidade
    email = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField()
    
    # Endereço
    rua = models.CharField(max_length=150)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100, default='Fortaleza')
    estado = models.CharField(max_length=2, default='CE')
    
    # Fidelidade e LGPD
    saldo_pontos = models.IntegerField(default=0) # Facilita a consulta no Totem
    aceite_termos = models.BooleanField(default=False)
    data_aceite_termos = models.DateTimeField(auto_now_add=True) # Auditoria LGPD

    def __str__(self):
        return self.nome_completo