# Generated by Django 5.2 on 2025-04-27 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_userprofile_address_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='logins',
            field=models.BigIntegerField(blank=True, db_column='logins', null=True),
        ),
    ]
