# Generated by Django 4.2.11 on 2024-08-01 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentacar', '0003_remove_carrental_testing_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrental',
            name='testing_field',
            field=models.TextField(blank=True, null=True),
        ),
    ]
