# Generated by Django 4.0.6 on 2022-09-14 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0006_alter_doctorsvisit_is_visit_done_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation',
            old_name='operation-name',
            new_name='operation_name',
        ),
    ]
