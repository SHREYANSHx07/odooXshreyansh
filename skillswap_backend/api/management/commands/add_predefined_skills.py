from django.core.management.base import BaseCommand
from api.models import Skill


class Command(BaseCommand):
    help = 'Add predefined skills to the database'

    def handle(self, *args, **options):
        predefined_skills = [
            'Python Programming',
            'JavaScript',
            'React Development',
            'Django Development',
            'Web Design',
            'Graphic Design',
            'Digital Marketing',
            'Content Writing',
            'Photography',
            'Video Editing',
            'Cooking',
            'Language Teaching',
            'Fitness Training',
            'Music Production',
            'Data Analysis',
            'Project Management',
            'UI/UX Design',
            'Mobile App Development',
            'SEO Optimization',
            'Social Media Management'
        ]

        created_count = 0
        for skill_name in predefined_skills:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            if created:
                created_count += 1
                self.stdout.write(f'Created skill: {skill_name}')
            else:
                self.stdout.write(f'Skill already exists: {skill_name}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(predefined_skills)} skills. {created_count} new skills created.')
        ) 