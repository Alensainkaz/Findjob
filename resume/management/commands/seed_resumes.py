"""Add 15 fictional demo resumes. Safe to run repeatedly: existing demo emails are skipped.

    python manage.py seed_resumes
"""
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from resume.cities import CITY_LABELS
from resume.models import SPECIALITY_CHOICES, Resume

DEMO_OWNER = 'demo@findy-job.com'
# Pexels stock portraits, one per demo resume; sources in demo_photos/CREDITS.md
PHOTO_DIR = Path(__file__).resolve().parent.parent / 'demo_photos'

# All people below are fictional; emails use the reserved example.com domain.
RESUMES = [
    ('Aruzhan', 'Seitkali', 'Nurlanovna', 'software_engineer', 'almaty',
     'Nazarbayev University, BSc Computer Science', '5 years: Python/Django backend at a fintech startup'),
    ('Daniyar', 'Abenov', 'Serikovich', 'data_analyst', 'astana',
     'KIMEP University, BSc Economics', '3 years: SQL and Power BI reporting for a retail chain'),
    ('Madina', 'Tulegenova', 'Askarovna', 'designer', 'almaty',
     'Kazakh National Academy of Arts, BA Design', '4 years: UI/UX for mobile banking apps'),
    ('Yerlan', 'Zhaksybekov', 'Muratovich', 'civil_engineer', 'shymkent',
     'South Kazakhstan University, BEng Civil Engineering', '7 years: residential construction site lead'),
    ('Aigerim', 'Omarova', 'Bauyrzhanovna', 'accountant', 'karaganda',
     'Karaganda University of Economics, BA Accounting', '6 years: IFRS reporting, 1C, tax filings'),
    ('Timur', 'Kassymov', 'Ruslanovich', 'web_developer', 'astana',
     'Astana IT University, BSc Software Engineering', '2 years: Vue.js and TypeScript frontend'),
    ('Dana', 'Nurpeisova', 'Yerbolovna', 'teacher', 'pavlodar',
     'Pavlodar Pedagogical University, BA English', '8 years: English teacher, IELTS preparation'),
    ('Arman', 'Sadykov', 'Kanatovich', 'sales_manager', 'aktobe',
     'Aktobe Regional University, BA Management', '5 years: B2B sales of industrial equipment'),
    ('Zarina', 'Bekova', 'Talgatovna', 'nurse', 'semey',
     'Semey Medical University, Nursing', '4 years: intensive care unit, city hospital'),
    ('Nurlan', 'Iskakov', 'Amanovich', 'electrician', 'oskemen',
     'East Kazakhstan Technical College, Electrical Systems', '9 years: industrial wiring and maintenance'),
    ('Kamila', 'Akhmetova', 'Dauletovna', 'lawyer', 'almaty',
     'Al-Farabi Kazakh National University, LLB', '5 years: corporate and contract law'),
    ('Askar', 'Mukhamedzhanov', 'Ermekovich', 'financial_analyst', 'astana',
     'Narxoz University, MSc Finance', '4 years: budgeting and investment analysis'),
    ('Saule', 'Dzhumabayeva', 'Kairatovna', 'translator', 'atyrau',
     'Eurasian National University, BA Translation', '6 years: English-Russian-Kazakh, oil and gas'),
    ('Bekzat', 'Ospanov', 'Nurzhanovich', 'mechanic', 'kostanay',
     'Kostanay Engineering College, Automotive Mechanics', '7 years: diesel engines and farm machinery'),
    ('Alina', 'Kim', 'Sergeevna', 'photographer', 'almaty',
     'Turan University, BA Journalism', '3 years: product and event photography'),
]


class Command(BaseCommand):
    help = 'Create 15 fictional demo resumes owned by a demo account'

    def handle(self, *args, **options):
        specialities = {key for key, _ in SPECIALITY_CHOICES}
        for row in RESUMES:
            if row[3] not in specialities:
                raise CommandError(f'Unknown speciality {row[3]!r}')
            if row[4] not in CITY_LABELS:
                raise CommandError(f'Unknown city {row[4]!r}')
            if max(len(row[5]), len(row[6])) > 100:
                raise CommandError(f'Education/experience over 100 chars for {row[0]} {row[1]}')

        User = get_user_model()
        with transaction.atomic():
            owner, created = User.objects.get_or_create(
                username=DEMO_OWNER, defaults={'email': DEMO_OWNER, 'is_active': True})
            if created:
                owner.set_unusable_password()
                owner.save()

            added = photos = 0
            for name, surname, father, spec, city, education, experience in RESUMES:
                resume, made = Resume.objects.get_or_create(
                    email=f'{name}.{surname}@example.com'.lower(),
                    defaults={
                        'name': name, 'surname': surname, 'father_name': father,
                        'speciality': spec, 'city': city,
                        'education': education, 'experience': experience,
                        'user': owner,
                    })
                added += made
                photo = PHOTO_DIR / f'{name}-{surname}.jpg'.lower()
                if not resume.image and photo.exists():
                    with photo.open('rb') as fh:
                        resume.image.save(photo.name, File(fh), save=True)
                    photos += 1
        self.stdout.write(self.style.SUCCESS(
            f'Added {added} demo resumes ({len(RESUMES) - added} already existed), '
            f'attached {photos} photos'))
