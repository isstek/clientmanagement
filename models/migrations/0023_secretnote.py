# Generated by Django 2.1.3 on 2019-04-24 17:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0022_person_phone_new'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecretNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactemail', models.EmailField(blank=True, max_length=120, null=True, verbose_name='Contact email address*')),
                ('note_text', models.TextField(blank=True, null=True, verbose_name='Secret note text*')),
                ('createdon', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('expireon', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Note expires on')),
                ('reads_left', models.IntegerField(blank=True, default=1, null=True, verbose_name='Count of reads left')),
                ('unid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
    ]
