# Generated by Django 5.1.4 on 2025-02-23 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaordenadores', '0006_alter_monitorgrafica_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='monitorgrafica',
            unique_together={('monitor', 'grafica')},
        ),
        migrations.AddField(
            model_name='monitorgrafica',
            name='es_monitor_gaming',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='monitorgrafica',
            name='resolucion_maxima',
            field=models.PositiveIntegerField(default=1080),
        ),
        migrations.AlterField(
            model_name='monitorgrafica',
            name='modo_conexion',
            field=models.CharField(choices=[('HDMI', 'HDMI'), ('DisplayPort', 'DisplayPort'), ('VGA', 'VGA'), ('DVI', 'DVI')], default='HDMI', max_length=15),
        ),
    ]
