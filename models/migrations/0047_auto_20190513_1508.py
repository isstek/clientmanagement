# Generated by Django 2.1.3 on 2019-05-13 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0046_auto_20190513_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemupdates',
            name='tittle',
            field=models.CharField(default='', max_length=160, verbose_name='Tittle'),
        ),
    ]