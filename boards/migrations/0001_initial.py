# Generated by Django 2.2 on 2020-03-20 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_type', models.CharField(choices=[('P', 'Personal'), ('T', 'Team')], max_length=1)),
                ('title', models.CharField(max_length=100)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BoardList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board_list', to='boards.Board')),
            ],
        ),
        migrations.CreateModel(
            name='ListCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('board_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_card', to='boards.BoardList')),
            ],
        ),
    ]