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
#service for verifying the domain admin
@csrf_exempt  
@api_view(['GET','POST'])
def FnVerifyDomain(request):
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    dbconn = db[settings.MONGO_DB]
    stream = StringIO(request.body)
    data = JSONParser().parse(stream)
    if request.method == 'POST':
        try:
            docs_list  = dbconn.system_js.fnVerifyDomain(data['domainUrl']);
        except:
            return Response('fail')
        return Response(docs_list)
    else:
        return Response(docs_list)  
#service function for adding new domain
@csrf_exempt  
@api_view(['GET','POST'])
def FnAddNewDomain(request):
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    dbconn = db[settings.MONGO_DB]
    stream = StringIO(request.body)
    data = JSONParser().parse(stream)
    if request.method == 'POST':
        try:
            docs_list  = dbconn.system_js.fnAddNewDomain(data['domainUrl'],data['urmId']);
        except:
            return Response('fail')
        return Response(json.dumps(docs_list, default=json_util.default))
    else:
        return Response(docs_list)
#service function for deactivating existing domain
@csrf_exempt  
@api_view(['GET','POST'])
def FnDeActivateDomain(request):
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    dbconn = db[settings.MONGO_DB]
    stream = StringIO(request.body)
    data = JSONParser().parse(stream)
    if request.method == 'POST':
        try:
            docs_list  = dbconn.system_js.fnDeActivateDomain(data['domainId'],data['urmId']);
        except:
            return Response('fail')
        return Response(json.dumps(docs_list, default=json_util.default))
    else:
        return Response(docs_list)
#service function to check the domain name already exists or not
@csrf_exempt  
@api_view(['GET','POST'])
def FnDomainNameExists(request):
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    dbconn = db[settings.MONGO_DB]
    stream = StringIO(request.body)
    data = JSONParser().parse(stream)
    if request.method == 'POST':
        try:
            docs_list  = dbconn.system_js.fnDomainNameExists(data['domainUrl']);
        except:
            return Response('fail')
        return Response(json.dumps(docs_list, default=json_util.default))
    else:
        return Response(docs_list)