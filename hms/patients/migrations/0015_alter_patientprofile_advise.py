# Generated by Django 4.0.6 on 2022-09-06 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0014_remove_patientprofile_advised_procedure_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprofile',
            name='advise',
            field=models.CharField(choices=[('Operation', 'Operation'), ('Admit', 'Admit'), ('Medication', 'Medication'), ('Discharged', 'Discharged'), ('Reports', 'Reports')], default='NA', max_length=50),
        ),
    ]
