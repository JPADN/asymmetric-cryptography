from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from OpenSSL import crypto
from django.contrib.postgres.fields import JSONField


class Post(models.Model):
    title = models.CharField(max_length=100)
    content: models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE) # Se eu deletar o usuário, deleto o post

    # Método para printar o title quando acesso objetos de um schema
    def __str__(self):
        return self.title

class Ac_certificado(models.Model):    
    cert_autoassinado = models.BinaryField()

class Certificados_emitidos(models.Model):
    certificado = models.BinaryField()
    serial = models.PositiveIntegerField(default=0)
    issuer = JSONField(default=dict)

class Contador(models.Model):
    pass
