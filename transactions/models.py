from django.db import models
from users.models import User

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('annule', 'Annulé'),
    )
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_as_provider')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_as_client')
    amount_total = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):
    TYPE_CHOICES = (
        ('gratuit', 'Gratuit'),
        ('pro', 'Pro'),
        ('premium', 'Premium'),
    )
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20)
