# Generated by Django 5.1.2 on 2024-11-28 07:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaordenadores', '0004_rename_grafica_grafica_grafica_procesadores'),
    ]

    operations = [
        migrations.AddField(
            model_name='procesador',
            name='placabase',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tiendaordenadores.placabase'),
        ),
    ]