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
from jobRelatedView import FileUploadView

#created by jihin
#For global values
@csrf_exempt
@api_view(['GET','POST'])
def LoadGlobalValuesView(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]

    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        response=dbconn.system_js.fnGetGlobals(data['key']);
        return Response(json.dumps(response, default=json_util.default))
    else:    
        return Response("failure")

#created by jihin
#For upload profile picture 
@csrf_exempt
@api_view(['GET','POST'])
def UploadProfilePicView(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]

    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)

        response=dbconn.system_js.fnUploadProfilePic(data['path'],ObjectId(data['urmId']));
        return Response(json.dumps(response, default=json_util.default))
    else:    
        return Response("failure")
