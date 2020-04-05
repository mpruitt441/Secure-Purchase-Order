from django.db import models
from django.contrib.auth.models import AbstractUser
#from Crypto.PublicKey import RSA

# Create your mod

class User(AbstractUser):
    is_supervisor = models.BooleanField('supervisor status', default=False)
    is_purchasing = models.BooleanField('purchasing department status', default=False)
    #keypair = RSA.generate(2048)



