from django.db import models
from django.db.models import Sum


class ApplicationParameters(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=200)


class DominatingFoot(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class ManagementAgency(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=200)
    transfermarkt_id = models.IntegerField(unique=True)
    transfermarkt_hyperlink = models.URLField(unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    description = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.description


class Country(models.Model):
    description = models.CharField(max_length=200)
    transfermarkt_id = models.IntegerField(unique=True)
    transfermarkt_hyperlink = models.URLField(unique=True)
    is_excluded = models.BooleanField(default=False)

    def get_not_excluded_leagues(self):
        return self.league_set.filter(is_excluded=False)


class League(models.Model):
    description = models.CharField(max_length=200)
    transfermarkt_id = models.CharField(unique=True, max_length=200)
    transfermarkt_hyperlink = models.URLField(unique=True)
    is_excluded = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.description

    def get_all_seasons(self):
        return self.season_set.all()


class Season(models.Model):
    description = models.CharField(max_length=200)
    begin_year = models.IntegerField()
    end_year = models.IntegerField()
    transfermarkt_hyperlink = models.URLField(unique=True)
    league = models.ForeignKey(League, on_delete=models.DO_NOTHING)
    all_teams_fetched = models.BooleanField(default=False)
    all_players_from_teams_fetched = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Queue(models.Model):
    number = models.IntegerField()
    transfermarkt_hyperlink = models.CharField(max_length=200)
    are_matches_fetched = models.BooleanField(default=False)
    season = models.ForeignKey(Season, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.season) + ' Queue ' + str(self.number)


class Match(models.Model):
    first_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="first_team")
    second_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="second_team")
    date = models.DateField(null=True)
    transfermarkt_hyperlink = models.URLField(unique=True)
    queue = models.ForeignKey(Queue, on_delete=models.DO_NOTHING)
    are_event_fetched = models.BooleanField(default=False)

    def __str__(self):
        return str(self.first_team) + ' vs ' + str(self.second_team)

    def get_season(self):
        return self.queue.season

    def get_transfermarkt_id_as_string(self):
        return str(self.transfermarkt_hyperlink.rsplit('/', 1)[1])


class Player(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateField(null=True)
    position = models.ForeignKey(Position, on_delete=models.DO_NOTHING, null=True)
    foot = models.ForeignKey(DominatingFoot, on_delete=models.DO_NOTHING, null=True)
    agency = models.ForeignKey(ManagementAgency, on_delete=models.DO_NOTHING, null=True)
    transfermarkt_id = models.IntegerField(unique=True)
    transfermarkt_hyperlink = models.URLField(unique=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name if self.last_name is not None else self.first_name

    def get_all_goals(self):
        return self.goal_set.all()

    def get_all_assists(self):
        return self.assist_set.all()

    def get_time_sum_from_all_matches(self):
        return self.matchplayer_set.all().aggregate(Sum('time'))['time__sum']


class TeamSeason(models.Model):
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    season = models.ForeignKey(Season, on_delete=models.DO_NOTHING)


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


class MatchPlayer(models.Model):
    time = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    match = models.ForeignKey(Match, on_delete=models.DO_NOTHING)

