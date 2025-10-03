import random
from django.core.management.base import BaseCommand
from users.models import User, Profile, UserContact

BURKINA_FIRST_NAMES = [
    "Issa", "Fanta", "Oumar", "Awa", "Blaise", "Fatoumata", "Souleymane",
    "Mariama", "Adama", "Rakoto", "Naba", "Salimata", "Yacouba", "Djeneba"
]

BURKINA_LAST_NAMES = [
    "Zongo", "Sawadogo", "Ouédraogo", "Kaboré", "Traoré", "Nacro", "Sankara",
    "Koma", "Kinda", "Sangaré"
]

ROLES = ['client', 'prestataire']

def random_phone_number():
    return "+226" + "".join(str(random.randint(0,9)) for _ in range(8))

class Command(BaseCommand):
    help = "Charge 20 utilisateurs fictifs burkinabés avec profils et contacts"

    def handle(self, *args, **options):
        for i in range(20):
            first_name = random.choice(BURKINA_FIRST_NAMES)
            last_name = random.choice(BURKINA_LAST_NAMES)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
            role = random.choice(ROLES)

            user = User.objects.create_user(
                email=email,
                password="Burkina2025!",
                is_active=True,
                is_staff=False,
                role=role
            )

            # Vérifier l'existence du profil avant création
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'geographic_zone': "Burkina Faso",
                    'bio': f"Profil fictif de {first_name} {last_name}",
                    'availability': True,
                    'subscription_status': "gratuit",
                    'verified_badge': random.choice([True, False]),
                }
            )
            if not created:
                profile.first_name = first_name
                profile.last_name = last_name
                profile.geographic_zone = "Burkina Faso"
                profile.bio = f"Profil fictif de {first_name} {last_name}"
                profile.availability = True
                profile.subscription_status = "gratuit"
                profile.verified_badge = random.choice([True, False])
                profile.save()

            # Création contacts
            phone_number = random_phone_number()
            UserContact.objects.create(
                user=user,
                contact_type='phone',
                value=phone_number,
                label='principal'
            )

            self.stdout.write(self.style.SUCCESS(
                f"Utilisateur créé: {email}, téléphone: {phone_number}, rôle: {role}"
            ))

        self.stdout.write(self.style.SUCCESS("20 utilisateurs burkinabés créés avec succès."))
