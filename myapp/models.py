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
import os
import urllib
import facebook
import json
import urllib2
import urlparse
import subprocess
import warnings
import oauth2 as oauth
import urlparse 
import oauth2 as oauth
import time
import simplejson
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
		        
		token = oauth.Token(key="f4062f5d-1955-494c-a6a8-9f594eaf18db",secret="52ed6665-8709-46d7-a272-d12a5c00c56d")
		 
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
		