from django.db import models


class ApplicationParameters(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=200)


class DominatingFoot(models.Model):
    description = models.CharField(max_length=50)


class ManagementAgency(models.Model):
    name = models.CharField(max_length=200)


class Team(models.Model):
    name = models.CharField(max_length=200)
    transfermarkt_id = models.IntegerField(unique=True)
    transfermarkt_hyperlink = models.URLField(unique=True)


class Position(models.Model):
    description = models.CharField(max_length=200)


class Country(models.Model):
    description = models.CharField(max_length=200)
    transfermarkt_id = models.IntegerField(unique=True)
    transfermarkt_hyperlink = models.URLField(unique=True)
    is_excluded = models.BooleanField(default=False)


class League(models.Model):
    description = models.CharField(max_length=200)
    transfermarkt_id = models.CharField(unique=True, max_length=200)
    transfermarkt_hyperlink = models.URLField(unique=True)
    is_excluded = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)


class Season(models.Model):
    description = models.CharField(max_length=200)
    begin_year = models.IntegerField()
    end_year = models.IntegerField()
    transfermarkt_hyperlink = models.URLField(unique=True)
    league = models.ForeignKey(League, on_delete=models.DO_NOTHING)


class Queue(models.Model):
    number = models.IntegerField()
    transfermarkt_hyperlink = models.CharField(max_length=200)
    is_data_fetched = models.BooleanField(default=False)
    season = models.ForeignKey(Season, on_delete=models.DO_NOTHING)


class Match(models.Model):
    first_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="first_team")
    second_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="second_team")
    date = models.DateField()
    transfermarkt_hyperlink = models.URLField(unique=True)


class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    position = models.ForeignKey(Position, on_delete=models.DO_NOTHING)
    foot = models.ForeignKey(DominatingFoot, on_delete=models.DO_NOTHING)
    agency = models.ForeignKey(ManagementAgency, on_delete=models.DO_NOTHING)
    transfermarkt_id = models.IntegerField(unique=True)
    transfermarkt_hyperlink = models.URLField(unique=True, null=True)


class PlayerTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    season = models.ForeignKey(Season, on_delete=models.DO_NOTHING)


class Goal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.DO_NOTHING)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)


class Assist(models.Model):
    match = models.ForeignKey(Match, on_delete=models.DO_NOTHING)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)


class MatchPlayers(models.Model):
    time = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    match = models.ForeignKey(Match, on_delete=models.DO_NOTHING)

