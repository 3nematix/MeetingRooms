# Generated by Django 3.1.3 on 2020-11-19 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201119_0303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='invitees',
            new_name='invites',
        ),
    ]
