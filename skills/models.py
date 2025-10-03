from django.db import models
from users.models import Profile

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserSkill(models.Model):
    LEVEL_CHOICES = (
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('expert', 'Expert'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    years_experience = models.PositiveIntegerField(default=0)
    details = models.TextField(blank=True)

class CV(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="cvs")
    file = models.FileField(upload_to='cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
