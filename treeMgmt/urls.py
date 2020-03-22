from django.urls import path
from . import views

urlpatterns = [path('getTree', views.getTree, name='getTree'),
               path('addFamilyMember', views.addFamilyMember, name='addFamilyMember'),
               path('addFamily',views.addFamily, name='addFamily')]
