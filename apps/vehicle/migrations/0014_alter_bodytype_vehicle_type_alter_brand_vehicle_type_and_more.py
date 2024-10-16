# Generated by Django 4.2.11 on 2024-08-30 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0013_vehicle_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodytype',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage'), (4, 'Component')], null=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage'), (4, 'Component')], null=True),
        ),
        migrations.AlterField(
            model_name='colour',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage'), (4, 'Component')], null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage'), (4, 'Component')], null=True),
        ),
        migrations.AlterField(
            model_name='vehicletypenumber',
            name='vehicle_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Car'), (2, 'Bike'), (3, 'Garage'), (4, 'Component')], null=True),
        ),
    ]
