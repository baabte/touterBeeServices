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
		access_token_page='CAACEdEose0cBAOIgBEVt07dxCZBfAqLCaA5nB41fZCEA3aUuIusw07CO1Igr66fRgzEZCLnZCvUmkIS9O2vFuWbdyT4D1zJXGOWrZChHH4YoWcygp6ybtNWSxXfjE0czl1QemzXC2zYFBleXJS69KEHPuniIOUHsNyB60LvXlYAYRsawGybb05zTL9pj3RS4sG4U9eWfVRgYp0a1EqjMg'
		FACEBOOK_APP_ID =resultObj['appId']
		FACEBOOK_APP_SECRET = resultObj['secretId']
		FACEBOOK_PROFILE_ID = resultObj['profileId']

		oauth_args = dict(client_id = FACEBOOK_APP_ID,client_secret = FACEBOOK_APP_SECRET,grant_type = 'client_credentials')
		attach = {
		"name": 'HEI THIS IS MY TESTING POST',
		"link": 'http://www.baabte.com',
		"caption": 'test post',
		"description": strip_tags(resultObj['content']),
		"picture" : 'http://image.slidesharecdn.com/baabtra-140528000621-phpapp01/95/baabtracom-and-massbaabcom-where-are-we-heading-3-638.jpg?cb=1401253759'#SOCIAL_IMG_PATH+str(inputObj['imageName']),
		#"page_token" : page_token,
		}

		facebook_graph = facebook.GraphAPI(access_token_page)
		#facebook_graph.get_object("me")
		try:
			response = facebook_graph.put_wall_post('', attachment=attach) #,profile_id = FACEBOOK_PROFILE_ID
			return response 
		except facebook.GraphAPIError as e:
			return e  		
	#function to share linked in content
	def fn_linkedin_share(self,resultObj):
		# Define CONSUMER_KEY, CONSUMER_SECRET,  
		# USER_TOKEN, and USER_SECRET from the credentials 
		# provided in your LinkedIn application

		# Instantiate the developer authentication class
		API_KEY = resultObj['appKey']
		API_SECRET = resultObj['apiSecretKey']
		RETURN_URL = 'http://localhost:8000/fnGetLinkedInAuthorisationCode?key='+API_KEY
		#authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,RETURN_URL, linkedin.PERMISSIONS.enums.values())
		#authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
		#application = linkedin.LinkedInApplication(authentication)
		authorisationCodeUrl=['curl','https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id='+API_KEY+'&scope=SCOPE&state=STATE&redirect_uri='+RETURN_URL]
		oauth_response = subprocess.Popen(authorisationCodeUrl,stdout = subprocess.PIPE,stderr = subprocess.PIPE).communicate()[0]
		#target=urllib2.urlopen(authentication.authorization_url)
		#authentication.authorization_code =  target.read()#[13:]
		
		#authentication.authorization_code ='AQWvmDHbnEKEHAfrjZYyads64QoXe8DxPDgo5WAdSRSusQ4YBrWBpLIBOncAd8r9bw3DqYQ-WxW6fmx2E9R-58eu9z32pwWws9XOLKwbr5N7oK7Yh1CF6lZFtBA3J_HTSWbbNKXEJ-2CHd_avaPMk17W0cbEFWPo-IiPHVYgVf7kF3ZB614'
		#token=authentication.get_access_token()
		# application = linkedin.LinkedInApplication(token=token)
		# # Pass it in to the app...
		# application.submit_share(resultObj['caption'], resultObj['title'], resultObj['content'], resultObj['link'], 'http://d.pr/3OWS')
		# {'updateKey': u'UNIU-8219502-5705061301949063168-SHARE',
 	# 	'updateURL': 'http://www.linkedin.com/updates?discuss=&amp;scope=8219502&amp;stype=M&amp;topic=5705061301949063168&amp;type=U&amp;a=aovi'}
		# Use the app....

		#application.get_profile()
		return authorisationCodeUrl  # open this url on your browser
		