# Generated by Django 4.2.11 on 2024-08-01 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiclewishlists',
            name='testing_field',
        ),
    ]
