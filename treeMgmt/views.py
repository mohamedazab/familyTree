from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from neo4j import GraphDatabase
from .models import Graph
# Create your views here.


def getTree(request):
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "au-12400301"
    h = HelloWorldExample(uri,user,password)

    h.get_family("hi there!")
    return HttpResponse(content='success', status=200)

def addNode(request):
    return HttpResponse(content='success', status=200)