from django.db import migrations, models

import resume.cities


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0017_speciality_slug_values'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='city',
            field=models.CharField(choices=resume.cities.CITY_CHOICES, db_index=True, default='', max_length=50),
            preserve_default=False,
        ),
    ]
