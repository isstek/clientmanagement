# Generated by Django 2.1.3 on 2019-05-22 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='API_key',
            new_name='APIKey',
        ),
    ]