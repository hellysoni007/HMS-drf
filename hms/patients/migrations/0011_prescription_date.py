# Generated by Django 4.0.6 on 2022-08-29 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0010_remove_prescription_medication_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
