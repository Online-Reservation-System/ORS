# Generated by Django 3.2.4 on 2021-06-10 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0004_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='AppUser',
        ),
    ]
