# Generated by Django 5.1.2 on 2024-12-16 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_mymodel_dropdown_field_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymodel',
            name='interval',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]