# Generated by Django 5.1.2 on 2024-12-11 17:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaordenadores', '0007_alter_grafica_memoriavram_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procesador',
            name='hilos',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='procesador',
            name='nucleos',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='procesador',
            name='potenciacalculo',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(20)]),
        ),
    ]