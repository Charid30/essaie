import random
from django.core.management.base import BaseCommand
from users.models import Profile
from skills.models import CV, Skill, UserSkill

class Command(BaseCommand):
    help = 'Créer des contacts aléatoires pour clients et prestataires, et CVs pour prestataires'

    CONTACT_TYPES = ['linkedin', 'facebook', 'email', 'phone', 'twitter']

    def handle(self, *args, **kwargs):
        # Exemple contacts
        example_contacts = {
            'linkedin': 'https://linkedin.com/in/example',
            'facebook': 'https://facebook.com/example',
            'email': 'user@example.com',
            'phone': '+123456789',
            'twitter': 'https://twitter.com/example',
        }

        profiles = Profile.objects.filter(user__role__in=['client', 'prestataire'])

        for profile in profiles:
            # Supprimer les anciens contacts pour ne pas dupliquer
            profile.user.contacts.all().delete()

            # Créer au moins 3 contacts différents pour chaque profil
            chosen_types = random.sample(self.CONTACT_TYPES, 3)
            for contact_type in chosen_types:
                value = example_contacts.get(contact_type)
                label = contact_type.capitalize()
                profile.user.contacts.create(contact_type=contact_type, value=value, label=label)

            # Si prestataire, créer aussi des CVs aléatoires
            if profile.user.role == 'prestataire':
                # Supprimer anciens CVs
                profile.cvs.all().delete()

                # Créer entre 1 et 3 CVs
                for i in range(random.randint(1, 3)):
                    description = f"CV généré automatique numéro {i+1} pour {profile.user.email}"
                    # Ici créer un fichier dummy placeholder (ou référencer un fichier vide statique si besoin)
                    # Pour l'exemple on met un fichier inexistant à remplacer par un vrai fichier
                    profile.cvs.create(
                        description=description,
                        file=f'cvs/placeholder{i+1}.pdf'
                    )

        self.stdout.write(self.style.SUCCESS('Contacts et CVs créés avec succès.'))
