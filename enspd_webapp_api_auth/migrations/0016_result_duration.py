# Generated by Django 5.0.4 on 2025-05-07 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enspd_webapp_api_auth', '0015_alter_evaluation_autor_alter_evaluation_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='duration',
            field=models.DateTimeField(default=None),
        ),
    ]
