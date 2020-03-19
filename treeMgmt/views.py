from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from neo4j import GraphDatabase
from .models import GraphConnection, basic_auth
import json

# Create your views here.


def getTree(request):
    params = QueryDict(request.META['QUERY_STRING'])
    if('family' in params.keys()):
        last_name = params['family']
        g = GraphConnection()
        result = g.get_family(last_name)
        return HttpResponse(content=json.dumps(result), status=200)
    else:
        return HttpResponse(content='failed', status=404)

def addNode(request):
    return HttpResponse(content='success', status=200)
