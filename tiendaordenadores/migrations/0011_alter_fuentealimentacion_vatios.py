# Generated by Django 5.1.2 on 2024-12-13 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaordenadores', '0010_alter_procesador_hilos_alter_procesador_nucleos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuentealimentacion',
            name='vatios',
            field=models.PositiveIntegerField(),
        ),
    ]
