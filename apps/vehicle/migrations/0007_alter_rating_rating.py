# Generated by Django 4.2.11 on 2024-08-04 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0006_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=2),
        ),
    ]
