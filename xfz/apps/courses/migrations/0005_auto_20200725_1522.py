# Generated by Django 2.2 on 2020-07-25 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_picture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='course',
            name='dispaly',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='coursecategory',
            name='dispaly',
            field=models.BooleanField(default=True),
        ),
    ]
