# Generated by Django 2.1.3 on 2019-04-29 15:49

import datetime
from models import secretnote
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0034_uploadedfileticket_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secretnote',
            name='expireon',
            field=models.DateField(blank=True, default=secretnote.calc_date, null=True, verbose_name='Note expires on'),
        ),
        migrations.AlterField(
            model_name='uploadedfileticket',
            name='for_ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='models.Ticket'),
        ),
    ]