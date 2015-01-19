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
class SocialFeatures(object):
	def fn_facebook_share(self,resultObj):
		access_token_page=resultObj['accessToken']
		FACEBOOK_APP_ID =resultObj['appId']
		FACEBOOK_APP_SECRET = resultObj['secretId']
		FACEBOOK_PROFILE_ID = resultObj['profileId']
		oauth_args = dict(client_id = FACEBOOK_APP_ID,client_secret = FACEBOOK_APP_SECRET,grant_type = 'client_credentials')
		oauth_response = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)).read()       
		attach = {
		"name": resultObj['title'],
		"link": resultObj['link'],
		"caption": resultObj['caption'],
		"description": strip_tags(resultObj['content']),
		"picture" : 'http://image.slidesharecdn.com/baabtra-140602041905-phpapp02/95/baabtracom-presentation-template-1-638.jpg?cb=1401700782'#SOCIAL_IMG_PATH+str(inputObj['imageName']),
		#"page_token" : page_token,
		}
		facebook_graph = facebook.GraphAPI(access_token_page)
		try:
			response = facebook_graph.put_wall_post('', attachment=attach) #,profile_id = FACEBOOK_PROFILE_ID
			return response  
		
		except facebook.GraphAPIError as e:
			return e
	#function to sharing content into LinkedIn
	def fn_linkedin_share(self,resultObj):
		# Define CONSUMER_KEY, CONSUMER_SECRET,  
		# USER_TOKEN, and USER_SECRET from the credentials 
		# provided in your LinkedIn application

		# Instantiate the developer authentication class
		API_KEY = '78balr8oe7bptc'
		API_SECRET = 'vVNOUMPdkuR4Y5ec'
		RETURN_URL = 'http://localhost:8000/view.py'
		#authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,RETURN_URL, linkedin.PERMISSIONS.enums.values())
		authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
		application = linkedin.LinkedInApplication(authentication)
		#authentication.authorization_code ='AQWvmDHbnEKEHAfrjZYyads64QoXe8DxPDgo5WAdSRSusQ4YBrWBpLIBOncAd8r9bw3DqYQ-WxW6fmx2E9R-58eu9z32pwWws9XOLKwbr5N7oK7Yh1CF6lZFtBA3J_HTSWbbNKXEJ-2CHd_avaPMk17W0cbEFWPo-IiPHVYgVf7kF3ZB614'
		#authentication.get_access_token()
		application = linkedin.LinkedInApplication(token='AQWvmDHbnEKEHAfrjZYyads64QoXe8DxPDgo5WAdSRSusQ4YBrWBpLIBOncAd8r9bw3DqYQ-WxW6fmx2E9R-58eu9z32pwWws9XOLKwbr5N7oK7Yh1CF6lZFtBA3J_HTSWbbNKXEJ-2CHd_avaPMk17W0cbEFWPo-IiPHVYgVf7kF3ZB614')
		# Pass it in to the app...
		application.submit_share('Posting from the API using JSON', 'A title for your share', None, 'http://www.baabtra.com', 'http://d.pr/3OWS')
		{'updateKey': u'UNIU-8219502-5705061301949063168-SHARE',
 		'updateURL': 'http://www.linkedin.com/updates?discuss=&amp;scope=8219502&amp;stype=M&amp;topic=5705061301949063168&amp;type=U&amp;a=aovi'}
		# Use the app....

		#application.get_profile()
		return authentication.authorization_url  # open this url on your browser
		