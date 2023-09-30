# Generated by Django 4.2.4 on 2023-09-26 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0026_publicreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='FIRFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='fir_files/')),
                ('crime_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crimeapp.crimereport')),
            ],
        ),
    ]
