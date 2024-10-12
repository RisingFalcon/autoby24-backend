# Generated by Django 4.2.11 on 2024-08-25 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentacar', '0005_rename_owner_carrental_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrental',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='carrental',
            name='model',
        ),
        migrations.AlterField(
            model_name='carimage',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_image', to='rentacar.carrental'),
        ),
    ]
