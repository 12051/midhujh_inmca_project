# Generated by Django 4.2.4 on 2023-10-19 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0041_alter_crimereport_status_alter_docreport_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inmate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inmate_name', models.TextField(blank=True, max_length=100, null=True)),
                ('inmate_id', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrisonReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc_prison', models.CharField(choices=[('kanjirappally', 'Kanjirappally'), ('changanassery', 'Changanassery')], max_length=100)),
                ('nat_crime', models.CharField(choices=[('misconduct', 'Inmate Misconduct'), ('breach', 'Security Breaches'), ('harm', 'Harm')], max_length=100)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('evidence_image', models.FileField(blank=True, null=True, upload_to='evidence_images/')),
                ('inmates', models.ManyToManyField(blank=True, to='crimeapp.inmate')),
            ],
        ),
    ]