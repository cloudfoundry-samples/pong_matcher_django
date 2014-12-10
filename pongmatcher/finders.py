from pongmatcher.models import Participant

class Match:
    @classmethod
    def get(cls, uuid):
        participants = Participant.objects.filter(match_uuid=uuid)
        if len(participants) > 0:
            return Match(uuid=participants[0].match_uuid,
                    match_request_1_uuid=participants[0].match_request_uuid,
                    match_request_2_uuid=participants[1].match_request_uuid)
        else:
            return None

    def __init__(self, uuid, match_request_1_uuid, match_request_2_uuid):
        self.uuid = uuid
        self.match_request_1_uuid = match_request_1_uuid
        self.match_request_2_uuid = match_request_2_uuid
