# Generated by Django 4.0 on 2022-08-19 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_applicationtag_historicalapplicationtag_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='application.applicationtag'),
        ),
    ]
