# Generated by Django 2.2 on 2020-03-01 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_newscomment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NewsComment',
        ),
    ]