# Generated by Django 4.2.11 on 2024-09-07 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0014_alter_bodytype_vehicle_type_alter_brand_vehicle_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_condition',
            field=models.IntegerField(blank=True, choices=[(1, 'New'), (2, 'Used'), (3, 'Demo'), (4, 'Classic'), (5, 'Accident')], null=True),
        ),
    ]
