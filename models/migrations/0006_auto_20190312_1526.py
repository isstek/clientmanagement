# Generated by Django 2.1.3 on 2019-03-12 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0005_auto_20190312_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkequipment',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='networkequipment', to='models.Client'),
        ),
    ]