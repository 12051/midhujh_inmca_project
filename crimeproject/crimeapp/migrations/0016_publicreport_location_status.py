# Generated by Django 4.2.4 on 2024-02-28 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0015_remove_crimereport_crimestatus_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicreport',
            name='location_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]