from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from OpenSSL import crypto
from django.contrib.postgres.fields import JSONField


class Ac_certificado(models.Model):    
    cert_autoassinado = models.TextField()
    serial = models.PositiveIntegerField(default=0)
    issuer = JSONField(default=dict)
    subject = JSONField(default=dict)


class Certificados_emitidos(models.Model):
    certificado = models.TextField()
    serial = models.PositiveIntegerField(default=0)
    issuer = JSONField(default=dict)
    subject = JSONField(default=dict)

class Contador(models.Model):
    pass
