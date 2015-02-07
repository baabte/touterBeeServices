from rest_framework.views import APIView
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from pymongo import Connection
import json
from bson import json_util
from StringIO import StringIO
from rest_framework.parsers import JSONParser
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
from django.core.mail import EmailMessage
import random
import string
from django.core.mail import send_mail
from django.template import Context, Template
from django.template.loader import render_to_string, get_template
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render
import datetime
from models import signup
#created by arun
#For applying for a job as candidate (Now it is open to all)
class companyRegisterView(APIView):
      parser_classes = (FileUploadParser,)


      def post(self, request, format=None):
          #connect to our local mongodb
          db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
          #get a connection to our database
          dbconn = db[settings.MONGO_DB]
          postdata=request.POST
          postdata['fksectorId']=ObjectId(postdata['fksectorId'])
          #postdata['fkcountryId']=ObjectId(postdata['fkcountryId'])
          #postdata['fkstateId']=ObjectId(postdata['fkstateId'])
          #postdata['fkdistrictId']=ObjectId(postdata['fkdistrictId'])
          postdata['loggedusercrmid']=ObjectId(postdata['loggedusercrmid'])
          postdata['password']=''.join([random.choice(string.digits + string.letters) for i in range(0, 6)])
          postdata['activationKey']=signup.fnActivationKeyGenerator(signup(),postdata['eMail']) #getting the account activation key
          postdata['keyExpires']=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S") #expire time           
    
          result = dbconn.system_js.fnComRegInsert(postdata)
          link=settings.HOST_ADDR+"activate/"+postdata['activationKey']

          file_obj = request.FILES['file']#['candidate']
          filename=result.get('name')
          path = default_storage.save(settings.FILEUPLOAD_PATH+'/companyLogo/'+filename, file_obj)
          filenameArray=path.split('/')
          actualfilename=filenameArray[len(filenameArray)-1]
          data = {
          'activation_link': link,
          'userName': postdata['eMail'],
          'user': postdata['companyName'],
          'password': postdata['password']
          }
          message = get_template(settings.TEMPLATE_DIRS[0]+'/ActivateAccount.html').render(Context(data))
          email = EmailMessage('Registered Successfully!! Verify your account',message, to=[postdata['eMail']])
          email.content_subtype = 'html'
          a=email.send()
          return Response(json.dumps(request.POST, default=json_util.default))
          #file_move_safe(file_obj, "/tmp/new_file")
          # ...
          # do some staff with uploaded file
          # ...
          #return Response(settings.LOGO_PATH+actualfilename)