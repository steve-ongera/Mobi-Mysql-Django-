# Generated by Django 5.1.2 on 2024-11-18 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_safaricom'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fuliza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('used', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.account')),
            ],
        ),
    ]