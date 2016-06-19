from django.db import models
from encrypted_fields import EncryptedTextField


class OFMUser(models.Model):
    username = models.CharField(max_length=255)
    password = EncryptedTextField()
