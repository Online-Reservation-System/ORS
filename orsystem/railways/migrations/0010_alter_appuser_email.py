# Generated by Django 3.2.4 on 2021-06-11 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0009_alter_appuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='email',
            field=models.EmailField(max_length=50),
        ),
    ]
