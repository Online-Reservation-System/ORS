# Generated by Django 3.2.4 on 2021-06-11 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0002_train'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('user_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='UserID')),
                ('name', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='train',
            name='trainid',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
