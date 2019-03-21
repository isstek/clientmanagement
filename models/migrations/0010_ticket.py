# Generated by Django 2.1.3 on 2019-03-18 16:50

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_auto_20190314_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdon', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('contactname', models.CharField(max_length=120, verbose_name='Contact name*')),
                ('contactphone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='Contact phone number')),
                ('contactemail', models.EmailField(max_length=120, verbose_name='Contact email address*')),
                ('title', models.CharField(max_length=120, verbose_name='Subject*')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description of the issue')),
                ('senderipaddress', models.GenericIPAddressField(verbose_name='Sender IP address')),
            ],
        ),
    ]