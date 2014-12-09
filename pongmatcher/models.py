from django.db import models

class MatchRequest(models.Model):
    uuid = models.CharField(max_length=200)
    player_uuid = models.CharField(max_length=200)

    def __str__(self):
        return "request: %(request)s\nfor player: %(player)s" % {
                "request": self.uuid,
                "player": self.player_uuid,
                }

    def match_id(self):
        return None

class Participant(models.Model):
    match_uuid = models.CharField(max_length=200)
    match_request_uuid = models.CharField(max_length=200)
    player_uuid = models.CharField(max_length=200)
    opponent_uuid = models.CharField(max_length=200)

    def __str__(self):
        return "match: %(match)s\nrequest: %(request)s\nplayer: %(player)s\nopponent: %(opponent)s" % {
                "match": self.match_uuid,
                "request": self.match_request_uuid,
                "player": self.player_uuid,
                "opponent": self.opponent_uuid
                }

