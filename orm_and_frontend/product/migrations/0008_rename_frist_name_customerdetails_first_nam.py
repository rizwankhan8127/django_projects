# Generated by Django 4.2.6 on 2024-02-15 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_customerdetails'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerdetails',
            old_name='frist_name',
            new_name='first_nam',
        ),
    ]
