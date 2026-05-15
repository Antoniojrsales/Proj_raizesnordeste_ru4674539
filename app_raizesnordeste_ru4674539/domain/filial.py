from django.db import models

class Filial(models.Model):
    id_filial = models.AutoField(primary_key=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.cidade} - {self.estado}"