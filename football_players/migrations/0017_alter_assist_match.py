# Generated by Django 3.2.2 on 2021-06-12 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football_players', '0016_rename_is_data_fetched_queue_are_matches_fetched'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assist',
            name='match',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='football_players.match'),
        ),
    ]