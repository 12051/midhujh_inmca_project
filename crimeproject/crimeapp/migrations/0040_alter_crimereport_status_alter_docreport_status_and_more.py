# Generated by Django 4.2.4 on 2023-10-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0039_alter_crimereport_status_alter_docreport_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crimereport',
            name='status',
            field=models.CharField(blank=True, choices=[('Crime Reported', 'Crime Reported'), ('Preliminary Investigation completed', 'Preliminary Investigation completed'), ('Inquiry and Investigation in progress', 'Inquiry and Investigation in progress'), ('Inquiry and Investigation completed', 'Inquiry and Investigation completed'), ('Arrest and Detention', 'Arrest and Detention'), ('Case Closure in progress', 'Case Closure in progress'), ('Case Closed', 'Case Closed')], default='Reported', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='docreport',
            name='status',
            field=models.CharField(blank=True, choices=[('Crime Reported', 'Crime Reported'), ('Preliminary Investigation completed', 'Preliminary Investigation completed'), ('Inquiry and Investigation in progress', 'Inquiry and Investigation in progress'), ('Inquiry and Investigation completed', 'Inquiry and Investigation completed'), ('Arrest and Detention', 'Arrest and Detention'), ('Case Closure in progress', 'Case Closure in progress'), ('Case Closed', 'Case Closed')], default='Reported', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='publicreport',
            name='status',
            field=models.CharField(choices=[('Crime Reported', 'Crime Reported'), ('Preliminary Investigation completed', 'Preliminary Investigation completed'), ('Inquiry and Investigation in progress', 'Inquiry and Investigation in progress'), ('Inquiry and Investigation completed', 'Inquiry and Investigation completed'), ('Arrest and Detention', 'Arrest and Detention'), ('Case Closure in progress', 'Case Closure in progress'), ('Case Closed', 'Case Closed')], default='Reported', max_length=100),
        ),
    ]
