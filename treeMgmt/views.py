from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from neo4j import GraphDatabase
from .models import GraphConnection
import json
from django.views.decorators.csrf import csrf_exempt
import uuid
# Create your views here.


def getTree(request):
    params = QueryDict(request.META['QUERY_STRING'])
    if('family' in params.keys()):
        g = GraphConnection()
        attributes = {'family': params['family']}
        result = g.getFamily(attributes)
        return HttpResponse(content=json.dumps(result), status=200)
    else:
        return HttpResponse(content='failed', status=404)



@csrf_exempt
def addFamily(request):
    # family attributes
    # 1 node representing a root for the family

    result ={}
    result['success'] = False
    if("family" in request.POST.keys()):
        id = uuid.uuid1()
        attributes = {'id': str(id), 'family': request.POST["family"]}
        g = GraphConnection()
        result = g.addFamily(attributes)
        return HttpResponse(content=json.dumps(result), status=200)

    return HttpResponse(content=json.dumps(result), status=500)


@csrf_exempt
def addFamilyMember(request):
    # family attributes
    # 1 node representing a root for the family
    print(request.body)
    # decode body 
    jsonBody = request.body.decode('utf8').replace("'", '"')
    # parse json body
    data = json.loads(jsonBody)
    id = uuid.uuid1()
    data['newNode']['id'] = str(id)
    print(type(data))
    print(data['newNode'])

    result = {'success':False}
    if("familyName" in data):
        g = GraphConnection()
        if('rootMember' in data):
            print("this is a root member")
            result = g.addMainNode(data)
        else:
            print("not a root member")
            result = g.addNode(data)
        return HttpResponse(content=json.dumps(result), status=200)

    return HttpResponse(content=json.dumps(result), status=500)
