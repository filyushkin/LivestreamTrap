# Generated by Django 5.1.2 on 2024-11-10 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_field', models.CharField(max_length=100)),
                ('dropdown_field', models.CharField(choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3'), ('option4', 'Option 4'), ('option5', 'Option 5')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i_d', models.CharField(max_length=11, verbose_name='Stream ID')),
                ('taskchannel_id', models.CharField(max_length=24, verbose_name='Channel ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('date', models.DateField(verbose_name='Дата')),
                ('path', models.CharField(max_length=100, verbose_name='Путь к стриму')),
                ('url', models.CharField(max_length=50, verbose_name='Ссылка на стрим')),
            ],
        ),
        migrations.CreateModel(
            name='TaskChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=30, verbose_name='Псевдоним')),
                ('name', models.CharField(max_length=60, verbose_name='Имя')),
                ('i_d', models.CharField(max_length=24, verbose_name='ID')),
            ],
        ),
    ]