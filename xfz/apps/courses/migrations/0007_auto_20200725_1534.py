# Generated by Django 2.2 on 2020-07-25 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20200725_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursecategory',
            old_name='dispaly',
            new_name='display',
        ),
    ]
