# Generated by Django 4.2.11 on 2024-08-10 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multimediafeature',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage')], null=True),
        ),
        migrations.AlterField(
            model_name='optionalfeature',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage')], null=True),
        ),
        migrations.AlterField(
            model_name='safetyassistancefeature',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage')], null=True),
        ),
        migrations.AlterField(
            model_name='standardfeature',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage')], null=True),
        ),
    ]
