# Generated by Django 4.2.11 on 2024-08-30 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0002_alter_multimediafeature_vehicle_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multimediafeature',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage'), (4, 'Component')], null=True),
        ),
        migrations.AlterField(
            model_name='optionalfeature',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage'), (4, 'Component')], null=True),
        ),
        migrations.AlterField(
            model_name='safetyassistancefeature',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage'), (4, 'Component')], null=True),
        ),
        migrations.AlterField(
            model_name='standardfeature',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage'), (4, 'Component')], null=True),
        ),
    ]
