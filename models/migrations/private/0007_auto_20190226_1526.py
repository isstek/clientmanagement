# Generated by Django 2.1.3 on 2019-02-26 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0006_auto_20190226_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, related_name='computer', to='models.Person'),
        ),
    ]
