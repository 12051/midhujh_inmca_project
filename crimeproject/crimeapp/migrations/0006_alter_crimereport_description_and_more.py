# Generated by Django 4.2.4 on 2024-01-11 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0005_crimereport_report_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crimereport',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='crimereport',
            name='reporter_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
