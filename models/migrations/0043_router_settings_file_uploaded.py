# Generated by Django 2.1.3 on 2019-05-13 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0042_auto_20190510_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='router',
            name='settings_file_uploaded',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]