# Generated by Django 3.1.3 on 2020-11-09 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insights', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='actors',
            new_name='users',
        ),
    ]