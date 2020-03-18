from django.urls import path
from . import views

urlpatterns = [path('getTree', views.getTree, name='getTree'),
               path('addNode', views.addNode, name='addNode')]
