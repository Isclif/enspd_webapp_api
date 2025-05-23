# Generated by Django 5.0.4 on 2025-04-18 17:57

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enspd_webapp_api_auth', '0006_alter_usermember_sexe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermember',
            old_name='time_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='usermember',
            old_name='employee_updater',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='usermember',
            old_name='time_updated',
            new_name='updated_at',
        ),
        migrations.AddField(
            model_name='usermember',
            name='updated_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usermember',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='usermember',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='usermember',
            name='status',
            field=models.CharField(choices=[('Etudiant', 'Etudiant'), ('Professeur', 'Professeur'), ('Admin', 'Admin'), ('ChefDepartement', 'ChefDepartement')], max_length=30),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructor_courses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='enspd_webapp_api_auth.course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='enspd_webapp_api_auth.department'),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='enspd_webapp_api_auth.course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('text', models.TextField()),
                ('answer', models.CharField(max_length=255)),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='enspd_webapp_api_auth.evaluation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('score', models.FloatField()),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='enspd_webapp_api_auth.evaluation')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='enspd_webapp_api_auth.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('student', 'course')},
            },
        ),
    ]
