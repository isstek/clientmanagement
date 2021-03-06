# Generated by Django 2.1.3 on 2019-04-18 19:09

from django.db import migrations
import phonenumber_field.modelfields


def transfer_phone_data(apps, schema_editor):
    Person = apps.get_model('models', 'Person')
    for person in Person.objects.all():
        person.phone_new = person.phone
        person.save()

class Migration(migrations.Migration):

    dependencies = [
        ('models', '0021_remove_client_phone_old'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='phone_new',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default=None, help_text='In the following format: +10000000000x0000, if you need extension', max_length=128, null=True, verbose_name='Phone Number'),
        ),
        migrations.RunPython(transfer_phone_data),
        migrations.RenameField(
            model_name='person',
            old_name='phone',
            new_name='phone_old',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='phone_new',
            new_name='phone',
        ),
        migrations.RemoveField(
            model_name='person',
            name='phone_old',
        ),
    ]
