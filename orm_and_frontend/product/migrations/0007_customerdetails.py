# Generated by Django 4.2.6 on 2024-02-13 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0006_ordertable'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frist_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('address_type', models.CharField(choices=[('home', 'HOME'), ('office', 'Office'), ('other', 'Other')], max_length=100)),
                ('full_address', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=100)),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
