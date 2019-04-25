# Generated by Django 2.1.3 on 2019-04-24 19:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0024_auto_20190424_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='secretnote',
            name='subject',
            field=models.CharField(default='test', max_length=120, verbose_name='Subject*'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='secretnote',
            name='expireon',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 5, 1, 19, 40, 58, 213642, tzinfo=utc), null=True, verbose_name='Note expires on'),
        ),
    ]
