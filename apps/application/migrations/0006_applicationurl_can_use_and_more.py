# Generated by Django 4.0 on 2023-06-23 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_applicationconfiguration_uses_jwt_validation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationurl',
            name='can_use',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='historicalapplicationurl',
            name='can_use',
            field=models.BooleanField(default=True),
        ),
    ]
