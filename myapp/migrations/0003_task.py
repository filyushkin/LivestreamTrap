# Generated by Django 5.1.2 on 2024-12-16 09:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_taskmodel_alter_mymodel_dropdown_field'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('interval', models.IntegerField(choices=[(1, '1 минута'), (5, '5 минут'), (10, '10 минут'), (30, '30 минут'), (60, '1 час')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_run', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]