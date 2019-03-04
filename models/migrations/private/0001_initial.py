# Generated by Django 2.1.3 on 2019-02-25 19:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import macaddress.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Client Name')),
                ('address', models.CharField(blank=True, default='', max_length=120, null=True, verbose_name='Client Address')),
                ('phone', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Phone Number')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Additional information')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkEquipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connection_type', models.CharField(choices=[('W', 'WiFi'), ('E', 'Ethernet'), ('N', 'No connection')], default='N', max_length=1, verbose_name='Netowrk connection type')),
                ('ip_type', models.CharField(choices=[('D', 'DHCP address'), ('L', 'Static address, local'), ('R', 'Static address, router'), ('N', 'No connection')], default='N', max_length=1, verbose_name='IP addressing type')),
                ('ip_address', models.GenericIPAddressField(blank=True, default='', null=True, verbose_name='IP Address')),
                ('mac_address', macaddress.fields.MACAddressField(blank=True, integer=False, max_length=17, null=True)),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Additional information')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=30, verbose_name='First Name')),
                ('lastname', models.CharField(max_length=30, verbose_name='Last Name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Phone Number')),
                ('annoyance', models.PositiveSmallIntegerField(default='0', validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Annoyance level')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Additional information')),
            ],
        ),
        migrations.CreateModel(
            name='WorksAt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maincontact', models.BooleanField(default=False, verbose_name='Main Contact?')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Client')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('networkequipment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='models.NetworkEquipment')),
                ('computername', models.CharField(max_length=30, verbose_name='Computer Name')),
                ('operatingsystem', models.CharField(blank=True, choices=[('W10', 'Windows 10'), ('W7', 'Windows 7'), ('WXP', 'Windows XP'), ('WO', 'Windows Other'), ('MJ', 'MacOS Majovang'), ('MHS', 'MacOS High Siera')], default='', max_length=3, null=True)),
            ],
            bases=('models.networkequipment',),
        ),
        migrations.AddField(
            model_name='person',
            name='employedby',
            field=models.ManyToManyField(related_name='employees', through='models.WorksAt', to='models.Client', verbose_name='Employed by'),
        ),
        migrations.AddField(
            model_name='networkequipment',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Client'),
        ),
        migrations.AddField(
            model_name='computer',
            name='user',
            field=models.ManyToManyField(null=True, related_name='computer', to='models.Person'),
        ),
    ]