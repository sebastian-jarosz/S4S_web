# Generated by Django 3.2.2 on 2021-06-08 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football_players', '0014_auto_20210603_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamSeason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='football_players.season')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='football_players.team')),
            ],
        ),
    ]
