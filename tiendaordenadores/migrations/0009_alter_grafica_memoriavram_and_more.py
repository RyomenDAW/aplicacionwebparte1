# Generated by Django 5.1.2 on 2024-12-11 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaordenadores', '0008_alter_procesador_hilos_alter_procesador_nucleos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grafica',
            name='memoriavram',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='grafica',
            name='potenciacalculo',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='procesador',
            name='hilos',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='procesador',
            name='nucleos',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='procesador',
            name='potenciacalculo',
            field=models.PositiveBigIntegerField(),
        ),
    ]
