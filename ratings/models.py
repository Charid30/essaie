from django.db import models
from users.models import User
from transactions.models import Transaction

class Rating(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    rated = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    rating_value = models.IntegerField()  # 1 to 5 
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
