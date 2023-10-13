# Generated by Django 4.2.4 on 2023-10-10 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0038_alter_evidencecrimereport_crime_idnum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crimereport',
            name='status',
            field=models.CharField(blank=True, choices=[('Crime Reported', 'Crime Reported'), ('Preliminary Investigation in progress', 'Preliminary Investigation in progress'), ('Preliminary Investigation completed', 'Preliminary Investigation completed'), ('Inquiry and Investigation in progress', 'Inquiry and Investigation in progress'), ('Inquiry and Investigation completed', 'Inquiry and Investigation completed'), ('Arrest and Detention', 'Arrest and Detention'), ('Case Closure in progress', 'Case Closure in progress'), ('Case Closed', 'Case Closed')], default='Reported', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='docreport',
            name='status',
            field=models.CharField(blank=True, choices=[('Crime Reported', 'Crime Reported'), ('Preliminary Investigation in progress', 'Preliminary Investigation in progress'), ('Preliminary Investigation completed', 'Preliminary Investigation completed'), ('Inquiry and Investigation in progress', 'Inquiry and Investigation in progress'), ('Inquiry and Investigation completed', 'Inquiry and Investigation completed'), ('Arrest and Detention', 'Arrest and Detention'), ('Case Closure in progress', 'Case Closure in progress'), ('Case Closed', 'Case Closed')], default='Reported', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='publicreport',
            name='status',
            field=models.CharField(choices=[('Crime Reported', 'Crime Reported'), ('Preliminary Investigation in progress', 'Preliminary Investigation in progress'), ('Preliminary Investigation completed', 'Preliminary Investigation completed'), ('Inquiry and Investigation in progress', 'Inquiry and Investigation in progress'), ('Inquiry and Investigation completed', 'Inquiry and Investigation completed'), ('Arrest and Detention', 'Arrest and Detention'), ('Case Closure in progress', 'Case Closure in progress'), ('Case Closed', 'Case Closed')], default='Reported', max_length=100),
        ),
    ]
