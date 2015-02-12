from django.db import models
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FileUploadParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from pymongo import Connection
from django.utils.html import strip_tags
from linkedin import linkedin
from django.db import models
import json
from bson import json_util
from StringIO import StringIO
from rest_framework.parsers import JSONParser
import os
import urllib
import json
import urllib2
import urlparse
import hashlib
import random
import facebook
import subprocess
import warnings
import oauth2 as oauth 
import time
import simplejson
# Create your models here.
# class Restaurant(object):
#     def __init__(self, id, name, address):
#         self.id = id
#         self.name = name
#         self.address = address

class UserMenuMapping(object):
	def __init__(self,id,fkRoleId,fkUserLoginId,fkCompanyId,fkEmployeeId,fkConsumerId,groups,createdDate,updatedDate,crmId,urmId,activeFlag):
		self.id=id
		self.fkRoleId=fkRoleId
		self.fkUserLoginId=fkUserLoginId
		self.fkCompanyId=fkCompanyId
		self.fkEmployeeId=fkEmployeeId
		self.fkConsumerId=fkConsumerId
		self.groups=groups
		self.createdDate=createdDate
		self.updatedDate=updatedDate
		self.crmId=crmId
		self.urmId=urmId
		self.activeFlag=activeFlag


# created by:Arun R Menon 
#on 07-06-14
class CompanyRegistration(object):	#model of company registration 
	def __init__(self,id,companyName,eMail,Place,Street,Phone,Mobile,userName,createdDate,updatedDate,crmId,urmId,activeFlag):
		self.id=id
		self.companyName=companyName
		self.eMail=eMail
		self.Place=Place
		self.Street=Street
		self.Phone=Phone
		self.Mobile=Mobile
		self.userName=userName
		self.createdDate=createdDate
		self.updatedDate=updatedDate
		self.crmId=crmId
		self.urmId=urmId
		self.activeFlag=activeFlag

class RegisteredCompany(object):	#model of registered Company
	def __init__(self,id,companyName,eMail,Place,Street,Phone,Mobile,userName,createdDate,updatedDate,crmId,urmId,activeFlag):
		self.id=id
		self.companyName=companyName
		self.eMail=eMail
		self.Place=Place
		self.Street=Street
		self.Phone=Phone
		self.Mobile=Mobile
		self.userName=userName
		self.createdDate=createdDate
		self.updatedDate=updatedDate
		self.crmId=crmId
		self.urmId=urmId
		self.activeFlag=activeFlag		
#signup class for signup related tasks		
class signup(object): #function to generate random activation key generator for account verification.
	def fnActivationKeyGenerator(self,userName):
		#We will generate a random activation key
		salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
		usernamesalt = userName
		if isinstance(usernamesalt, unicode):
			usernamesalt = usernamesalt.encode('utf8')
		activationKey= hashlib.sha1(salt+usernamesalt).hexdigest()
		return activationKey
class SocialFeatures(object):
	# def fn_facebook_share(self,resultObj):
	# 	page_token='CAACEdEose0cBAE7zjo5m0fTDONbgLmAB6kMPrMZC1pn3U4TzQD7pQlazUz7yXA9C0BrHKirWOb5ZAbh7XRcViao7ZCvPKJJsRKHxen0jInVw6kvVZBeiAOFfIgLmTi0FiYb2St76c8pV2olM2cIZBohlxpt2y8QEK8yj4NZBFAFKvYz8PRdKeS42kxkBDq9PYXpdRI1p9CqUytRVmPn7BZC'
	# 	access_token_page='CAACEdEose0cBALvNbMckdZAdtha0SHKX3nGoVVKIh4AUw9BUmB8XBNojpXC2OhriWTQqatsoMJMP513LytZAv53QLfelHfeWzAZBvC7AgJASHo64fryp7vkbR84qZAhCPPHsBmYPDzPpoz9ZCSH7azLO5qv1FgQQapGuTSG2XSyzRVKxCC2A5FEa3Thq52rIDuSaz0uH6zkPGSKY78KmQ'
	# 	FACEBOOK_APP_ID =resultObj['appId']
	# 	FACEBOOK_APP_SECRET = resultObj['secretId']
	# 	FACEBOOK_PROFILE_ID = resultObj['profileId']

	# 	oauth_args = dict(client_id = FACEBOOK_APP_ID,client_secret = FACEBOOK_APP_SECRET,grant_type = 'client_credentials')

	# 	oauth_response = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)).read()       

	# 	attach = {"name":"Hello world","link":"http://www.baabtra.com","caption":"test post","description":"some test","picture":"http://www.baabtra.com/assets/images/logo/baabtralogo.png"}

	# 	# facebook_graph = facebook.GraphAPI(access_token=access_token_page)
	 
 #  #       #facebook_graph.get_object("me")
	# 	# try:
	# 	# 	response = facebook_graph.put_wall_post('', attachment=attach,profile_id=FACEBOOK_PROFILE_ID) #,profile_id = FACEBOOK_PROFILE_ID
	# 	# 	return response 
	# 	# except facebook.GraphAPIError as e:
	# 	# 	return e
	# 	oauth_curl_cmd = ['curl','https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
	# 	oauth_response = subprocess.Popen(oauth_curl_cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE).communicate()[0]
	# 	#return urlparse.parse_qs(str(oauth_response))['access_token'][0]
	# 	try:
	# 		oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
	# 	except KeyError:
	# 		return 'Unable to grab an access token!'
    		
	# 	facebook_graph = facebook.GraphAPI(oauth_access_token)


	# 	# Try to post something on the wall.
	# 	try:
	# 		fb_response = facebook_graph.put_wall_post(message='Tessadasdasd post here www.baabtra.com',attachment={},profile_id = FACEBOOK_PROFILE_ID) #100007982954778,attachment=attach
	# 		return fb_response
	# 	except facebook.GraphAPIError as e:
	# 		return 'Something went wrong:', e, e.message
	# #function to sharing content into facebook temp
	def fn_facebook_share(self,resultObj):
		access_token_page='CAACEdEose0cBAPLSNAMJrDZBCIwuKpBxRcqNF4j4qLZBqvcNMMguzx0CTRayu8c7WY4mjYvU1SJ0X8JYxpoHCIv3xGbZCGaF7gJYrPJJ5oHiPOcMBiq9eq1WZCmyeXYrxXjdMl3F7PldiWvlpIJhJc2ak1HGZBZC8W1rTejTlsZA7CLTsXEUZCksFGot5cd3fP7HytQJnHo3SbwEwtJ05jCCom2LiZAPB340ZD'
		FACEBOOK_APP_ID =resultObj['appId']
		FACEBOOK_APP_SECRET = resultObj['secretId']
		FACEBOOK_PROFILE_ID = resultObj['profileId']

		oauth_args = dict(client_id = FACEBOOK_APP_ID,client_secret = FACEBOOK_APP_SECRET,grant_type = 'client_credentials')
		attach = {
		"name": 'HEI THIS IS MY TESTING POST',
		"link": 'http://www.baabtra.com',
		"caption": 'test post',
		"description": strip_tags(resultObj['content']),
		"picture" : 'http://baabtra.com/assets/images/logo/baabtralogo.png'#SOCIAL_IMG_PATH+str(inputObj['imageName']),
		#"page_token" : page_token,
		}

		facebook_graph = facebook.GraphAPI(access_token_page)
		#facebook_graph.get_object("me")
		try:
			response = facebook_graph.put_wall_post('', attachment=attach) #,profile_id = FACEBOOK_PROFILE_ID
			return response 
		except facebook.GraphAPIError as e:
			return e  		

	def fn_linkedin_share(self,resultObj):
		url = "http://api.linkedin.com/v1/people/~/shares"
	 
		consumer = oauth.Consumer(key=resultObj['appKey'],secret=resultObj['apiSecretKey'])
		client = oauth.Client(consumer)        
		token = oauth.Token(key="73ec3208-1d95-407c-9586-ffef4cdd23fa",secret="216ea01a-44c7-45e6-bd68-56df152d1cd3")
		 
		client = oauth.Client(consumer, token)
		body = {"comment":strip_tags(resultObj['content']),
		"content":{
		"title":resultObj['title'],
		"submitted_url":"www.baabtra.com",
		"submitted_image_url":'http://baabtra.com/assets/images/logo/baabtralogo.png'
		},
		"visibility":{"code":"anyone"}
		}
		           
		 
		resp, content = client.request(url, 'POST', body=simplejson.dumps(body), headers={'Content-Type':'application/json'})
		return resp,content