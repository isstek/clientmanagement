# Generated by Django 2.1.3 on 2019-03-07 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='operatingsystem',
            field=models.CharField(choices=[('W10', 'Windows 10'), ('W8', 'Windows 8'), ('W7', 'Windows 7'), ('WS19', 'Windows Server 2019'), ('WS16', 'Windows Server 2016'), ('WS12', 'Windows Server 2012'), ('WS08', 'Windows Server 2008'), ('WS03', 'Windows Server 2003'), ('MJ', 'MacOS Majovang'), ('MHS', 'MacOS High Siera'), ('MS', 'MacOS Siera'), ('WXP', 'Windows XP'), ('WO', 'Windows Other'), ('MO', 'MacOS Other'), ('O', 'Other')], default='W10', max_length=4),
        ),
    ]
