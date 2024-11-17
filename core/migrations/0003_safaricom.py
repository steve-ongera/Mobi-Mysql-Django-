# Generated by Django 5.1.2 on 2024-11-17 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_transaction_receiver'),
    ]

    operations = [
        migrations.CreateModel(
            name='Safaricom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50)),
                ('id_number', models.CharField(max_length=20, unique=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('date_of_birth', models.DateField()),
            ],
        ),
    ]