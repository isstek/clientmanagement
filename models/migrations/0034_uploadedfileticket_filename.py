# Generated by Django 2.1.3 on 2019-04-26 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0033_auto_20190426_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfileticket',
            name='filename',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]