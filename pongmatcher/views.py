from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from pongmatcher.models import MatchRequest, Participant
from pongmatcher.serializers import MatchRequestSerializer
from pongmatcher.finders import Match

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def wipe(request):
    if request.method == 'DELETE':
        MatchRequest.objects.all().delete()
        Participant.objects.all().delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)

@csrf_exempt
def match_request_list(request):
    return HttpResponse(status=404)

@csrf_exempt
def match_request_detail(request, uuid):
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        writeable_data = dict(data.items() | [('id', uuid)])
        serializer = MatchRequestSerializer(data=writeable_data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        else:
            return HttpResponse(status=422)
    elif request.method == 'GET':
        try:
            match_request = MatchRequest.objects.get(uuid=uuid)
            serializer = MatchRequestSerializer(match_request)
            return JSONResponse(serializer.data)
        except MatchRequest.DoesNotExist:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def match_detail(request, uuid):
    match = Match.get(uuid)
    if match:
        return JSONResponse(match)
    else:
        return HttpResponse(status=404)
