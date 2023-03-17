# Generated by Django 4.1.7 on 2023-03-17 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('railapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_name', models.CharField(max_length=256)),
                ('created_date', models.DateTimeField()),
                ('closed_date', models.DateTimeField(blank=True, null=True)),
                ('is_readonly', models.BooleanField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='roles',
            options={'verbose_name': 'Роль', 'verbose_name_plural': 'Роли'},
        ),
        migrations.AlterModelOptions(
            name='stations',
            options={'verbose_name': 'Станция', 'verbose_name_plural': 'Станции'},
        ),
        migrations.CreateModel(
            name='StationList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_id', models.IntegerField()),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='railapp.stations')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField()),
                ('chat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='railapp.chatlist')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
