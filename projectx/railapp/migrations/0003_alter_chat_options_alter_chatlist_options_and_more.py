# Generated by Django 4.1.7 on 2023-03-23 13:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('railapp', '0002_chatlist_alter_roles_options_alter_stations_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'verbose_name': 'Чат', 'verbose_name_plural': 'Чат'},
        ),
        migrations.AlterModelOptions(
            name='chatlist',
            options={'verbose_name': 'Список чатов', 'verbose_name_plural': 'Список чатов'},
        ),
        migrations.AlterModelOptions(
            name='stationlist',
            options={'verbose_name': 'Маршрутный лист', 'verbose_name_plural': 'Маршрутные листы'},
        ),
        migrations.RemoveField(
            model_name='stations',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='stations',
            name='start_date',
        ),
        migrations.AddField(
            model_name='customuser',
            name='number_route',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='number_wagon',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='stationlist',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stationlist',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stationlist',
            name='type',
            field=models.CharField(choices=[('D', 'Прямой'), ('R', 'Обратный')], default='D', max_length=1),
        ),
    ]