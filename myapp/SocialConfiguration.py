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
from models import signup #importing model class for getting the custom functions related to this view
from django.core.mail import send_mail
from django.template import Context, Template
from django.template.loader import render_to_string, get_template
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from models import SocialFeatures #importing the socialfetaure model class
import datetime
import os

#Author      : Akshath kumar M.
#Description : To load the verified domains for configuration
@csrf_exempt
@api_view(['GET','POST'])
def FnLoadDomainForConfig(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
   
    #return Response({"companyId":companyId,"name":name}) 
    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        result =  dbconn.system_js.fnLoadDomainForConfig(data['urmId'])
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")

#Author      : Akshath kumar M.
#Description : To load the script injector for touter bee. 
@csrf_exempt
@api_view(['GET','POST'])
def FnLoadTBeeConfig(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    clnSocialConfigDetails = dbconn['clnSocialConfigDetails']
    #return Response({"companyId":companyId,"name":name}) 
    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        #result = list(clnSocialConfigDetails.find({'domainName':str(data['urmId']),'fkWebsiteId':str(data['websiteId'])}));
        result = dbconn.system_js.fnLoadSocialConfigDetails(data['domainName']);
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")      

#Author      : Akshath kumar M.
#Description : To load the script injector for touter bee. 
@csrf_exempt
@api_view(['GET','POST'])
def FnSaveSocialConfigDetails(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    #clnSocialConfigDetails = dbconn['clnSocialConfigDetails']
    if request.method == 'POST':      
        data =request.POST

        #data = JSONParser().parse(stream)
        #if(request.FILES.length>0):
        file_obj = request.FILES['file']#['candidate']
        
        result = dbconn.system_js.FnSaveSocialConfigDetails(data);
        if file_obj!=null:
            extension = file_obj.content_type.split('/')[0]
            filename=result.get('pic')
            if(default_storage.exists(settings.FILEUPLOAD_PATH+'/socialConfigImages/'+str(filename))):
                #if os.path.exists(self.path(name)):
                #    os.remove(self.path(name))
                path = default_storage.save(settings.FILEUPLOAD_PATH+'/socialConfigImages/'+str(filename), file_obj)
                filenameArray=path.split('/')
                actualfilename=filenameArray[len(filenameArray)-1]
            else:
                default_storage.delete(settings.FILEUPLOAD_PATH+'/socialConfigImages/'+str(filename))
                path = default_storage.save(settings.FILEUPLOAD_PATH+'/socialConfigImages/'+str(filename), file_obj)
                filenameArray=path.split('/')
                actualfilename=filenameArray[len(filenameArray)-1]
                filename = str(filename) + str(file_obj)
                if not os.path.exists(settings.FILEUPLOAD_PATH+'/socialConfigImages/'+str(filename)): #checking if for the directory already exists or not
                    os.makedirs(settings.FILEUPLOAD_PATH+'/socialConfigImages/'+str(filename))
            
            return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")      
#Author      : Akshath kumar M.
#Description : To activate thesocial feature at the time selected element event
@csrf_exempt
@api_view(['GET','POST'])
def FnActivateEvent(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    #UserLoginCollection = dbconn['clnUserLogin']
   
    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        inputObj=data['inputObj'] #input object for posting 
               
        try:
            nameOfFn=getattr(SocialFeatures,inputObj['featureFunction']) #converting the string to dynamic function
            result=nameOfFn(SocialFeatures(),inputObj) #calling the dynamic function
            return Response(result)  
        except ValueError:
            return Response(ValueError)  

#Author      : Akshath kumar M.
#Description : To activate thesocial feature at the time selected element event
# @csrf_exempt
# @api_view(['GET','POST'])
# def fnfacebookshare(request):
#     #connect to our local mongodb
#     db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
#     #get a connection to our database
#     dbconn = db[settings.MONGO_DB]
#     #UserLoginCollection = dbconn['clnUserLogin']
   
#     if request.method == 'POST':
#         stream = StringIO(request.body)
#         data = JSONParser().parse(stream)
#         inputObj=data['inputObj'] #input object for posting 
#         page_token=''
#         access_token_page=''
#         FACEBOOK_APP_ID = ''
#         FACEBOOK_APP_SECRET = ''
#         FACEBOOK_PROFILE_ID = ''

#         oauth_args = dict(client_id = FACEBOOK_APP_ID,client_secret = FACEBOOK_APP_SECRET,grant_type = 'client_credentials')

#         oauth_response = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)).read()       

#         attach = {
#         "name": 'Hello world',
#         "link": 'www.baabte.com',
#         "caption": 'test post',
#         "description": strip_tags(inputObj['content']),
#         "picture" : 'http://image.slidesharecdn.com/baabtra-140528000621-phpapp01/95/baabtracom-and-massbaabcom-where-are-we-heading-3-638.jpg?cb=1401253759'#SOCIAL_IMG_PATH+str(inputObj['imageName']),
#         #"page_token" : page_token,
#         }

#         facebook_graph = facebook.GraphAPI(access_token_page)
#         #facebook_graph.get_object("me")
#         try:
#             response = facebook_graph.put_wall_post('', attachment=attach) #,profile_id = FACEBOOK_PROFILE_ID
#             return Response(response)  
#         except facebook.GraphAPIError as e:
#             return Response(e)  

@csrf_exempt
@api_view(['GET','POST'])
def FnLoadChannels(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    clnSocialConfigDetails = dbconn['clnChannels']
    #return Response({"companyId":companyId,"name":name}) 
    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        try:
            result =  dbconn.system_js.fnLoadChannels(data['domainId'])
        except Exception as e:
            return Response(str(e))
        return Response(json.dumps(result, default=json_util.default))
    else:        
        return Response("failure")      
        
@csrf_exempt
@api_view(['GET','POST'])
def fnLoadBroadcastTypeTemplate(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    #return Response({"companyId":companyId,"name":name}) 
    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        try:
            result =  dbconn.system_js.fnGetBroadcastTypeTemplate(data['channelId'],data['broadcastTypeId'],data['urmId'],data['domainId'],data['currentPage'],data['elementId'])
        except Exception as e:
            return Response(str(e))
        
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")
