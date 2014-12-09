from django.db import models
import uuid

class MatchRequest(models.Model):
    uuid = models.CharField(max_length=200)
    player_uuid = models.CharField(max_length=200)

    def __str__(self):
        return "request: %(request)s\nfor player: %(player)s" % {
                "request": self.uuid,
                "player": self.player_uuid,
                }

    def match_id(self):
        participants = Participant.objects.filter(match_request_uuid=self.uuid)
        if len(participants) == 0:
            return None
        else:
            return participants[0].match_uuid

    def persist_participants(self):
        opponent_request = self.find_opponent_request()

        if opponent_request:
            match_uuid = uuid.uuid4()
            Participant.objects.create(
                match_uuid=match_uuid,
                match_request_uuid=opponent_request.uuid,
                player_uuid=opponent_request.player_uuid,
                opponent_uuid=self.player_uuid
            )
            Participant.objects.create(
                match_uuid=match_uuid,
                match_request_uuid=self.uuid,
                player_uuid=self.player_uuid,
                opponent_uuid=opponent_request.player_uuid
            )

    def find_opponent_request(self):
        requests = MatchRequest.objects.raw('''SELECT * FROM pongmatcher_matchrequest
            WHERE player_uuid <> %s
            AND uuid NOT IN (SELECT match_request_uuid FROM pongmatcher_participant)
            AND player_uuid NOT IN
            (SELECT opponent_uuid FROM pongmatcher_participant WHERE player_uuid =  %s)''',
            [self.player_uuid, self.player_uuid])
        try:
            return requests[0]
        except IndexError:
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

