# Generated by Django 3.2.4 on 2021-06-16 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='amount',
            field=models.BigIntegerField(default=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='seats',
            field=models.BigIntegerField(default=450),
            preserve_default=False,
        ),
    ]
