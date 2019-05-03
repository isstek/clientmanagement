# Generated by Django 2.1.3 on 2019-05-03 16:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import models.tools as modelstools
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0036_uploadedfilecomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainTool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdon', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('name', models.CharField(max_length=80, verbose_name='Client Name')),
                ('public', models.BooleanField(default=False, verbose_name='Public tool')),
                ('unid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Description')),
            ],
        ),
        migrations.AlterField(
            model_name='printer',
            name='prmonth',
            field=models.IntegerField(blank=True, default=5, null=True, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)], verbose_name='Recieved Month (enter a number)'),
        ),
        migrations.CreateModel(
            name='FileTool',
            fields=[
                ('maintool_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='models.MainTool')),
                ('filename', models.CharField(max_length=100, verbose_name='Filename')),
                ('uplfile', models.FileField(max_length=255, null=True, upload_to=modelstools.upload_to_file_tool, verbose_name='File')),
                ('version', models.CharField(blank=True, default='', max_length=50, verbose_name='Version')),
            ],
            bases=('models.maintool',),
        ),
        migrations.CreateModel(
            name='LinkTool',
            fields=[
                ('maintool_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='models.MainTool')),
                ('url', models.URLField(max_length=255, verbose_name='Link')),
            ],
            bases=('models.maintool',),
        ),
    ]
