# Generated by Django 2.1.3 on 2019-04-26 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0028_auto_20190426_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFileTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdon', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('uplfile', models.FileField(max_length=255, upload_to='')),
                ('for_ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Ticket')),
            ],
        ),
    ]
