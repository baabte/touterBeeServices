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
import datetime
#created by  : Akshath kumar M
#description : For signup the user details.

@csrf_exempt  
@api_view(['GET','POST'])
def FnUserSignup(request):
	#connect to our local mongodb
	db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
	#get a connection to our database
	dbconn = db[settings.MONGO_DB]
	userMenuCollection = dbconn['tblUser']

	if request.method == 'POST':
		stream = StringIO(request.body)#reads the data passed along with the request
		data = JSONParser().parse(stream)#converts to json
		loginCredentials={}
		loginCredentials=data['signupData'] #getting the signup data
		SignupData=data
		try:
			x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
			if x_forwarded_for:
				real_ip = x_forwarded_for.split(',')[0]
			else:
				real_ip = request.META.get('REMOTE_ADDR')
			SignupData['ip']=real_ip
			SignupData['activationKey']=signup.fnActivationKeyGenerator(signup(),loginCredentials['email']) #getting the account activation key
			SignupData['keyExpires']=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S") #expire time			
			docs_list  = dbconn.system_js.fnUserSignup(SignupData)
			link=settings.HOST_ADDR+"activate/"+SignupData['activationKey']
			data = {
			'activation_link': link,
			'user_name': loginCredentials['email'],
			'user': loginCredentials['fullName']
			}
			message = get_template(settings.TEMPLATE_DIRS[0]+'/ActivateAccount.html').render(Context(data))
			email = EmailMessage('Registered Successfully!! Verify your account',message, to=[loginCredentials['email']])
			email.content_subtype = 'html'
			a=email.send()
			#print unicode(message).encode('utf8')
			#send_mail('Registered Successfully!! Verify your account', '', 'touter Bee <no-reply@touterbee.com>', [loginCredentials['email']], html_message=message,fail_silently=False)
		except ValueError:
			return Response(ValueError)    
		return Response(json.dumps(docs_list, default=json_util.default)) #dumps corresponding data in the response
	else:
		return Response({"result":"failed"})

#service for checking user name already registered  or not
#Author: Akshath kumar M.     
@csrf_exempt
@api_view(['GET','POST'])
def FnCheckEmailExists(request):
	#connect to our local mongodb
	db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
	#get a connection to our database
	dbconn = db[settings.MONGO_DB]

	if request.method == 'POST':      
		stream = StringIO(request.body)
		data = JSONParser().parse(stream)
		result = dbconn.system_js.fnUserNameValid(data['email'])
		return Response(json.dumps(result, default=json_util.default))            
	else:
		return Response("failure")

#Account verification key generator function
@csrf_exempt
@api_view(['GET','POST'])
def activation(request, key):
	activation_expired = False
	already_active = False
	#connect to our local mongodb
	db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
	#get a connection to our database
	dbconn = db[settings.MONGO_DB]
	clnUserLogin = dbconn['clnUserLogin']
	try:
		result  = dbconn.system_js.fnGetUserInfoForAccVerification(key)
		keyExpires=result.get('keyExpires')
		accVerifyFlag=result.get('accountVerificationFlag')
		userLoginId=result.get('_id')
		crmId=result.get('crmId')
		if accVerifyFlag == False:
			if datetime.datetime.now() >  datetime.datetime.strptime(keyExpires,'%Y-%m-%d %H:%M:%S'):
				activation_expired = True #Display : offer to user to have another activation link (a link in template sending to the view new_activation_link)
				new_activation_link(self,result.get('userName'),userLoginId,crmId)
				
			else: #Activation successful
				activation_expired = True
				dbconn.system_js.fnUpdateActivationFlag(userLoginId,crmId)

		#If user is already active, simply display error message
		else:
			already_active = True #Display : error message
			return render(request, settings.TEMPLATE_DIRS[0]+'/Failure.html', locals())
		return render(request, settings.TEMPLATE_DIRS[0]+'/Activation.html', locals())
	except ValueError:
		return Response(ValueError)
		
#function to send new activation link while previous one is already expires.
def new_activation_link(self,userName,user_id,crmId):
	activation_key = signup.fnActivationKeyGenerator(signup(),userName)
	key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
	dbconn.system_js.fnUpdateActivationKey(user_id,activation_key,key_expires,crmId)
	link=settings.HOST_ADDR+"activate/"+activation_key
	data = {
	'activation_link': link,
	'user_name': userName	
	}
	message = get_template(settings.TEMPLATE_DIRS[0]+'/ResendActivationKey.html').render(Context(data))
	email = EmailMessage('Verify your account',message, to=[userName])
	email.content_subtype = 'html'
	#a=email.send()
	return "success"