# Generated by Django 4.2.4 on 2023-09-26 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0022_rename_delay_docreport_delay_report_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docreport',
            name='status',
        ),
    ]
