# Generated by Django 2.1.3 on 2019-02-26 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20190226_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkequipment',
            name='connection_type',
            field=models.CharField(choices=[('N', 'No connection'), ('E', 'Ethernet'), ('W', 'WiFi')], default='N', max_length=1, verbose_name='Netowrk connection type'),
        ),
    ]