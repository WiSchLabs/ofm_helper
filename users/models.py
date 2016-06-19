from django.contrib.auth.models import AbstractUser
from django.db import models
from encrypted_fields import EncryptedTextField


class OFMUser(AbstractUser):
    ofm_username = models.CharField(max_length=255, null=True, blank=True)
    ofm_password = EncryptedTextField(null=True, blank=True)
