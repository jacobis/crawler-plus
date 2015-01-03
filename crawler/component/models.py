from django.db import models

class KeyManager(models.Model):
    GOOGLE_PLUS = 'GP'
    SERVICE_CHOICES = (
        (GOOGLE_PLUS, 'Google Plus'),
    )
    service = models.CharField(max_length=2, choices=SERVICE_CHOICES, default=GOOGLE_PLUS)
    key = models.CharField(max_length=200)
    note = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)