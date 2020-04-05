from django.db import models
from django.utils import timezone
from spo import settings
from django.urls import reverse
from datetime import datetime
import users

class order(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_ordered = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    # Supervisor Access
    approved = models.BooleanField(default=False)
    approvedBy = models.CharField(max_length=100)
    dateApproved = models.CharField(max_length=100)

    # Purchasing Department Access
    purchased = models.BooleanField(default=False)
    purchasedBy = models.CharField(max_length=100)
    datePurchased = models.CharField(max_length=100)

    # Create digest fields: https://stackoverflow.com/questions/51682594/python-django-how-to-create-hash-fields-inside-django-models-py
    signedPurchase = models.CharField(max_length=1000)
    signedSupervisor = models.CharField(max_length=1000)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('order-detail', kwargs={'pk': self.pk})