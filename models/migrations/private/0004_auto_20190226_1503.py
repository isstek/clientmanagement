# Generated by Django 2.1.3 on 2019-02-26 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0003_auto_20190226_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='manufacturer',
            field=models.CharField(choices=[('D', 'DELL'), ('H', 'HP'), ('L', 'Lenovo'), ('G', 'Apple'), ('A', 'Asus'), ('S', 'Sony'), ('C', 'Acer'), ('O', 'Other')], default='D', max_length=1),
        ),
        migrations.AddField(
            model_name='computer',
            name='model',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='computer',
            name='recdata',
            field=models.DateField(blank=True, null=True, verbose_name='Recieved date'),
        ),
        migrations.AddField(
            model_name='computer',
            name='serialnumber',
            field=models.CharField(blank=True, default='', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='operatingsystem',
            field=models.CharField(choices=[('W10', 'Windows 10'), ('W8', 'Windows 8'), ('W7', 'Windows 7'), ('WS6', 'Windows Server 2019'), ('WS6', 'Windows Server 2016'), ('WS2', 'Windows Server 2012'), ('WS08', 'Windows Server 2008'), ('WS03', 'Windows Server 2003'), ('WSO', 'Windows Other'), ('MJ', 'MacOS Majovang'), ('MHS', 'MacOS High Siera'), ('MHS', 'MacOS Siera'), ('MHS', 'MacOS Other'), ('WXP', 'Windows XP'), ('WO', 'Windows Other'), ('MO', 'MacOS Other'), ('O', 'Other')], default='W10', max_length=4),
        ),
    ]
