#---------------------------
#Sample service
#created by : Akshath kumar M
#Created on : 04-10-14
#-----------------------------

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import Connection
#from models import UserMenuMapping
from serializers import MongoAwareEncoder
from datetime import datetime
import json
from bson import json_util
from StringIO import StringIO
from rest_framework.parsers import JSONParser
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template

#service for loading the domains of specific admin user
#Author: Akshath kumar M.     
@csrf_exempt
@api_view(['GET','POST'])
def FnLoadDomainList(request):
	#connect to our local mongodb
	db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
	#get a connection to our database
	dbconn = db[settings.MONGO_DB]

	if request.method == 'POST':      
		stream = StringIO(request.body)
		data = JSONParser().parse(stream)
		try:
			result = dbconn.system_js.fnLoadDomainList(data['urmId'])
	           
		except Exception as e:
			return Response(str(e))
		return Response(json.dumps(result, default=json_util.default)) 

	else:
		return Response("failure")