from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission


class CustomUserManager(BaseUserManager):
    """
    Gestionnaire personnalisé pour créer un utilisateur avec email comme identifiant unique.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L’email doit être renseigné')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser doit avoir is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser doit avoir is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    ROLE_CHOICES = (
        ('prestataire', 'Prestataire'),
        ('client', 'Client'),
        ('admin', 'Administrateur'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text="Les groupes auxquels appartient l'utilisateur.",
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Permissions spécifiques de cet utilisateur.',
        related_query_name='custom_user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ContactType(models.TextChoices):
    EMAIL = 'email', 'Email'
    PHONE = 'phone', 'Numéro de téléphone'
    LINKEDIN = 'linkedin', 'LinkedIn'
    WHATSAPP = 'whatsapp', 'WhatsApp'
    OTHER = 'other', 'Autre'


class UserContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    contact_type = models.CharField(max_length=20, choices=ContactType.choices)
    value = models.CharField(max_length=255)
    label = models.CharField(max_length=100, blank=True, null=True)  # pro, perso etc.

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'contact_type', 'value')

    def __str__(self):
        return f"{self.user.email} - {self.get_contact_type_display()}: {self.value}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    geographic_zone = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    availability = models.BooleanField(default=True)
    subscription_status = models.CharField(max_length=20, default='gratuit')
    verified_badge = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
