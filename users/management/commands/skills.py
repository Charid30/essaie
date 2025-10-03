import random
from django.core.management.base import BaseCommand
from users.models import Profile
from skills.models import Skill, UserSkill

class Command(BaseCommand):
    help = 'Créer aléatoirement des compétences pour les prestataires'

    def handle(self, *args, **kwargs):
        # Liste de compétences exemples, à adapter ou ajouter
        example_skills = [
            ('Python', 'Langage de programmation', 'Développement'),
            ('Django', 'Framework web Python', 'Framework'),
            ('React', 'Bibliothèque frontend', 'Frontend'),
            ('Docker', 'Conteneurisation', 'DevOps'),
            ('AWS', 'Cloud Computing', 'Infrastructure'),
            ('Vue.js', 'Framework Javascript', 'Frontend'),
            ('SQL', 'Base de données relationnelles', 'Database'),
            ('Git', 'Gestion de version', 'Outils'),
        ]

        # Création ou récupération des compétences exemples en base
        skills_objects = []
        for name, desc, category in example_skills:
            skill_obj, created = Skill.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'category': category}
            )
            skills_objects.append(skill_obj)

        prestataires = Profile.objects.filter(user__role='prestataire')
        levels = ['debutant', 'intermediaire', 'expert']

        for profile in prestataires:
            # Nombre de compétences à créer entre 3 et 5
            nb_skills = random.randint(3, 5)

            # Random choice distinct skills
            skills_sample = random.sample(skills_objects, min(nb_skills, len(skills_objects)))

            for skill in skills_sample:
                # S'assurer de ne pas dupliquer la compétence
                if not UserSkill.objects.filter(profile=profile, skill=skill).exists():
                    UserSkill.objects.create(
                        profile=profile,
                        skill=skill,
                        level=random.choice(levels),
                        years_experience=random.randint(0, 10),
                        details=f"Compétence générée automatiquement pour {profile.user.email}"
                    )

        self.stdout.write(self.style.SUCCESS('Création aléatoire des compétences terminée.'))
