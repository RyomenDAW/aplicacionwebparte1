# Generated by Django 5.1.2 on 2024-12-11 17:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaordenadores', '0005_procesador_placabase'),
    ]

    operations = [
        migrations.AddField(
            model_name='grafica',
            name='placabase',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tiendaordenadores.placabase'),
        ),
    ]
