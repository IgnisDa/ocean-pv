# Generated by Django 3.1a1 on 2020-07-20 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='receive_emails',
            field=models.BooleanField(default=True),
        ),
    ]
