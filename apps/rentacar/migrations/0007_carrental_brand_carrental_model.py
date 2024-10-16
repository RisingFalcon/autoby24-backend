# Generated by Django 4.2.11 on 2024-08-25 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0013_vehicle_banner'),
        ('rentacar', '0006_remove_carrental_brand_remove_carrental_model_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrental',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicle.brand'),
        ),
        migrations.AddField(
            model_name='carrental',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicle.model'),
        ),
    ]
