# Generated by Django 4.2.11 on 2024-08-10 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0010_alter_colour_name_alter_colour_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='listing_type',
            field=models.IntegerField(choices=[(1, 'Rent'), (2, 'Sale')], default=2),
        ),
    ]
