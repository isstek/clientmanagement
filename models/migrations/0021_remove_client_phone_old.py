# Generated by Django 2.1.3 on 2019-04-18 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0020_auto_20190418_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='phone_old',
        ),
    ]
