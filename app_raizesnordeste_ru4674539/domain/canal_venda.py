from django.db import models

class CanalVenda(models.Model):
    id_canal = models.AutoField(primary_key=True)
    nome_canal = models.CharField(max_length=20) # App, Totem, Balcão

    def __str__(self):
        return self.nome_canal