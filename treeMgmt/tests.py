from django.test import TestCase
from .models import GraphConnection
# Create your tests here.
class familyMembersTest(TestCase):


    def testRetreiveMembers(self):
        attributes = {'family':"Elzohairy"}
        g = GraphConnection()
        result = g.getFamily(attributes)
        print(result)

    def testAddMember(self):
        x = 1
        print(x)