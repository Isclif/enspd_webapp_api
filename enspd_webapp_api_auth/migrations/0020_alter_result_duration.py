# Generated by Django 5.0.4 on 2025-05-07 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enspd_webapp_api_auth', '0019_alter_result_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='duration',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
