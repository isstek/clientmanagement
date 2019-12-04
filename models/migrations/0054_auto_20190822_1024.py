# Generated by Django 2.2.3 on 2019-08-22 14:24

from django.db import migrations, models
import models.wikiarticle as wikimodels


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0053_auto_20190813_1401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wikiarticle',
            old_name='createdon',
            new_name='updatedon',
        ),
        migrations.AlterField(
            model_name='wikiarticle',
            name='updatedon',
            field=models.DateTimeField(default=wikimodels.time_now, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='secretnote',
            name='reads_max',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Maximum number of reads left'),
        ),
        migrations.AlterField(
            model_name='wikiarticle',
            name='postedon',
            field=models.DateTimeField(default=wikimodels.time_now, verbose_name='Creation time'),
        ),
    ]