# Generated by Django 2.2 on 2020-05-28 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20200322_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='parent',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
