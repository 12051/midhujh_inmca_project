# Generated by Django 4.2.4 on 2023-09-30 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0027_firfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='docreport',
            name='status',
            field=models.CharField(choices=[('Reported', 'Reported'), ('FIR Verified', 'FIR Verified'), ('Investigation in progress', 'Investigation in progress'), ('Completed', 'Completed')], default='Reported', max_length=100),
        ),
        migrations.AddField(
            model_name='publicreport',
            name='status',
            field=models.CharField(choices=[('Reported', 'Reported'), ('FIR Verified', 'FIR Verified'), ('Investigation in progress', 'Investigation in progress'), ('Completed', 'Completed')], default='Reported', max_length=100),
        ),
    ]