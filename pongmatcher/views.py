from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

@csrf_exempt
def wipe(request):
    if request.method == 'DELETE':
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)

@csrf_exempt
def match_request_list(request):
    return HttpResponse(status=404)

@csrf_exempt
def match_request_detail(request, uuid):
    return HttpResponse(status=404)
