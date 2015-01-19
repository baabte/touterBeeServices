#---------------------------
#Sample service
#created by : Akshath kumar M
#Created on : 04-10-14
#-----------------------------

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
from models import SocialFeatures #importing the socialfetaure model class
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

@csrf_exempt  
@api_view(['GET','POST'])
def InsertUserMenu(request):                                   #for Inserting menu items for specific user
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    clnUserMenuMapping = dbconn['clnUserMenuMapping']

    if request.method == 'GET':
        #get our collection
        UserMenuMappingList = []
        
        docs_list  = list(clnUserMenuMapping.find())
        return Response(json.dumps(docs_list, default=json_util.default))
    elif request.method == 'POST':   #for post request
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        #data["fkMenuId"]=ObjectId(data["fkMenuId"])
        for menu in data["menus"]:
           menu['fkMenuId']=ObjectId(menu['fkMenuId'])
           for sub_menu in menu['childMenuStructure']:
               sub_menu['fkMenuId']=ObjectId(sub_menu['fkMenuId'])
               pass
           pass
        try:
            docs_list  = dbconn.system_js.fnSaveUserMenus(ObjectId(data['fkUrmId']),ObjectId(data["fkUserRoleMappingId"]),ObjectId(data["fkMenuRegionId"]),data["menus"]) 
        except:
            return Response(json.dumps("", default=json_util.default))
        return Response(StringIO(docs_list))

@csrf_exempt  
@api_view(['GET','POST'])
def UserRoleMenuMappingView(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    userMenuCollection = dbconn['tblUserMenuMapping']

    if request.method == 'GET':
        #get our collection
        UserMenuMappingList = []
        docs_list  = list(userMenuCollection.find())
        #return Response(json.dumps(docs_list, default=json_util.default))
        #for r in userMenuCollection.find():
        #    UserMenuMappingView = UserMenuMapping(r["_id"],r['fkRoleId'],r['fkUserLoginId'],r['fkCompanyId'],r['fkEmployeeId'],r['fkConsumerId'],r['groups'],r['createdDate'],r['updatedDate'],r['crmId'],r['urmId'],r['activeFlag'])
        #    UserMenuMappingList.append(UserMenuMappingView)
        #serializedList = UserMenuMappingSerializer(UserMenuMappingList, many=True)
        
        return Response(json.dumps(docs_list, default=json_util.default))
    elif request.method == 'POST':
        #get data from the request and insert the record
        #received_json_data=json.loads(request.body)
        #name = request.POST["_content"]
        #address = 'calicut' #request.POST["address"]
        try:
            userMenuCollection.insert({"fkUserRoleMappingId":100,"menuStructure": [{"fkmenuRegionId": 1,"regionMenuStructure": [{"fkMenuId": 1,"MenuName": "sample","MenuIcon": "fa_users","childMenuStructure": [{ }] }] }],"createdDate": datetime.now(),"updatedDate": datetime.now(),"crmId": 111,"urmId": 111,"activeFlag": 1})
        except:
            return Response(response.POST)
        #for r in restaurantCollection.find():
        #    restaurant = Restaurant(r["_id"],r["name"],r["address"])
        #    restaurants.append(restaurant)
        #serializedList = RestaurantSerializer(restaurants, many=True)
        return Response({"result":"success"})

@csrf_exempt  
@api_view(['GET','POST'])
def FnGetCompanyDetailsView(request):
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    dbconn = db[settings.MONGO_DB]
    stream = StringIO(request.body)
    data = JSONParser().parse(stream)
    if request.method == 'POST':
        try:
            docs_list  = dbconn.system_js.fnGetCompanyDetails(data['roleId'],data['companyId'],data['range'],data['prefix']);
        except:
            return Response(request.body)
        return Response(json.dumps(docs_list, default=json_util.default))
    else:
        return Response(docs_list)       
# #created by Arun.R.Menon
# #on 07-10-14
# @csrf_exempt
# @api_view(['GET','POST'])
# def CompanyRegistrationView(request):
#     #connect to our local mongodb
#     db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
#     #get a connection to our database
#     dbconn = db[settings.MONGO_DB]
#     #companyCollection = dbconn['clnCompany']
#     #userloginCollection = dbconn['clnUserLogin']
#     if request.method == 'POST':      
#         stream = StringIO(request.body)
#         data = JSONParser().parse(stream)
#         data['fksectorId']=ObjectId(data['fksectorId'])
#         data['fkcountryId']=ObjectId(data['fkcountryId'])
#         data['fkstateId']=ObjectId(data['fkstateId'])
#         data['fkdistrictId']=ObjectId(data['fkdistrictId'])
#         data['loggedusercrmid']=data['loggedusercrmid']
#         result = dbconn.system_js.fnComRegInsert(data);
#         email=result.get('cmail')
#         email = EmailMessage('Company Registered','Welcome to baabtra.com', to=[email])
#         email.send()
#         return Response(json.dumps(result, default=json_util.default))
#     else:        
#         return Response("failure")


#START===============================================================JIHIN RAJU===================================================================

#created by JIHIN RAJU
#on 07-10-14
@csrf_exempt  
@api_view(['GET','POST'])
def GetAllRolesView(request):#for get all the roles based on company_id
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    dbconn = db[settings.MONGO_DB]
    if request.method == 'POST':
        stream = StringIO(request.body)#reads the data passed along with the request
        data = JSONParser().parse(stream)#converts to json
        try:
            docs_list  = dbconn.system_js.fnGetAllRoles(data['rm_id'],ObjectId(data['cmp_id']),data['range'],data['roleVal']);
        except:
            return Response(request.body)    
        return Response(json.dumps(docs_list, default=json_util.default)) #dumps corresponding data in the response
    else:
        return Response(docs_list)

#created by JIHIN RAJU
#on 26-11-14
@csrf_exempt  
@api_view(['GET','POST'])
def FnLoadTopLevelRolesView(request):#for get all the roles based on company_id
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    dbconn = db[settings.MONGO_DB]
    if request.method == 'POST':
        #stream = StringIO(request.body)#reads the data passed along with the request
        #data = JSONParser().parse(stream)#converts to json
        try:
            docs_list  = dbconn.system_js.fnLoadTopLevelRoles();
        except:
            return Response(request.body)    
        return Response(json.dumps(docs_list, default=json_util.default)) #dumps corresponding data in the response
    else:
        return Response(docs_list)        

#created by JIHIN RAJU 
#on 07-10-14
@csrf_exempt  
@api_view(['GET','POST'])
def GetRoleMenusView(request):#for get all menus of selected user
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    dbconn = db[settings.MONGO_DB]
    if request.method == 'POST':
        stream = StringIO(request.body)#reads the data passed along with the request
        data = JSONParser().parse(stream)#converts to json
        try:
            docs_list  = dbconn.system_js.fnGetCurrentMenusById(data['fkRoleId'],data['type']);
        except:
            return Response(request.body)
        return Response(json.dumps(docs_list, default=json_util.default,sort_keys=True)) #dumps corresponding data in the response
    else:
        return Response(request.body)

#created by JIHIN RAJU
#on 07-10-14
@csrf_exempt  
@api_view(['GET','POST'])
def GetAllMenusView(request):#for get all menus of loged user
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    dbconn = db[settings.MONGO_DB]
    stream = StringIO(request.body)#reads the data passed along with the request
    data = JSONParser().parse(stream)#converts to json
    if request.method == 'POST':
        try:
            docs_list  = dbconn.system_js.fnGetCurrentMenusById(ObjectId(data['rm_id']),data['type']);
        except:
            return Response(request.body)
        return Response(json.dumps(docs_list, default=json_util.default,sort_keys=True)) #dumps corresponding data in the response
    else:
        return Response(request.body)

#created by JIHIN RAJU
#on 05-11-14
@csrf_exempt  
@api_view(['GET','POST'])
def FnGetCompanyDetailsJiView(request):#for get company details
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    dbconn = db[settings.MONGO_DB]
    stream = StringIO(request.body)#reads the data passed along with the request
    data = JSONParser().parse(stream)#converts to json
    if request.method == 'POST':
        try:
            docs_list  = dbconn.system_js.fnGetCompanyDetailsJi(data['range'],data['cmp_name']);
        except:
            return Response(request.body)
        return Response(json.dumps(docs_list, default=json_util.default)) #dumps corresponding data in the response
    else:
        return Response(docs_list)

#created by JIHIN RAJU
#on 07-10-14
@csrf_exempt  
@api_view(['GET','POST'])
def SaveNewRoleMenu(request): #for Insert or update menu items for specific user and role
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    dbconn = db[settings.MONGO_DB]
    if request.method == 'POST':
        stream = StringIO(request.body)#reads the data passed along with the request
        data = JSONParser().parse(stream)#converts to json
        response=""
        for menu in data["menus"]:
            menu['fkMenuId']=ObjectId(menu['fkMenuId'])
            for sub_menu in menu['childMenuStructure']:
                sub_menu['fkMenuId']=ObjectId(sub_menu['fkMenuId'])
                for sub_menu_sub in sub_menu['childMenuStructure']:
                    response="Not Allowed"
                    pass
                pass
        if response=="":
            try:            
                response=dbconn.system_js.fnSaveUserMenuMapping(data['rm_id'],data['role_id'],data['menus']); 
                response=dbconn.system_js.fnSaveRoleMenuMapping(data['rm_id'],data['role_id'],data['menus']);
            except:
                return Response(json.dumps("", default=json_util.default))
        pass
        return Response(StringIO(response))
    else:
        return Response(request.body)

#END===============================================================JIHIN RAJU=========================================================================
     
#------------------------------
#created by anu
#---------------------------
@csrf_exempt  
@api_view(['GET','POST'])
def GetMenuItems(request):                #for Inserting menu items for specific user
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    userMenuCollection = dbconn['clnUserMenuMapping']
    if request.method == 'GET':
        #get our collection
        UserMenuMappingList = []
        docs_list  = list(userMenuCollection.find())
        return Response({"name":"success"})      
    elif request.method == 'POST':
        stream = StringIO(request.body)  #reads the data passed along with the request
        data = JSONParser().parse(stream)   #converts to json
        docs_list  = dbconn.system_js.fnGetMenuItemsById(ObjectId(data['fkUserRoleMappingId'])); #calls the stored js function to find the corresponding menu

        try:
            return Response(json.dumps(docs_list, default=json_util.default)) #dumps corresponding data in the response
        except:
            return Response(json.dumps("", default=json_util.default))
       
        return Response(json.dumps(docs_list, default=json_util.default));

#-----------------------------


@csrf_exempt  
@api_view(['GET','POST'])
def LoadUsers(request): #Loading All the users based on compny id supplied
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        try:
            docs_list  = dbconn.system_js.fnSearchUsers(data['companyId'],data['prefix'],data["range"]);
        except:
            return Response(json.dumps("", default=json_util.default))
        return Response(json.dumps(docs_list, default=json_util.default)) #return the response here
    else:
        return Response("")

@csrf_exempt  
@api_view(['GET','POST'])
def LoadExMenuItems4AUMMapping(request): #Loading the existing user menu items
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        try:
            docs_list  = dbconn.system_js.fnLoadExMenusForUsers(data['fkUserRoleMappingId'],data['companyId'],data['roleId']);
        except:
            return Response(json.dumps("", default=json_util.default))
        return Response(json.dumps(docs_list, default=json_util.default))
    else:
        return Response("Get") #dbconn.system_js.myAddFunction(2,2)
@csrf_exempt  
@api_view(['GET','POST'])
def LoadMenuItems4AUMMapping(request): #Loding the Menu items for adding specific user
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    clnRoleMenuMapping = dbconn['clnRoleMenuMapping']

    if request.method == 'POST':

        try:
            stream = StringIO(request.body)
            data = JSONParser().parse(stream)
            #data['fkRoleId']=ObjectId(data['fkRoleId'])
            docs_list  = dbconn.system_js.fnGetCurrentRoleMenus(data['fkRoleId']);            
        except:
            return Response(json.dumps("", default=json_util.default))
        return Response(json.dumps(docs_list, default=json_util.default))
    else:
        return Response({"result":"success"})


    

##created by Arun.R.Menon
#on 09-10-14
@csrf_exempt
@api_view(['GET','POST'])
def RegisteredCompanyView(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    #companyCollection = dbconn['clnCompany']

    if request.method == 'POST':
        #get our collection
        try:
            companyList=dbconn.system_js.fnViewRegisteredCompany()
        except:
            return Response("error")
        return Response(json.dumps(companyList, default=json_util.default))
    else:        
        return Response("failure")

#created by Arun.R.Menon
#on 13-10-14
@csrf_exempt
@api_view(['GET','POST'])
def CompanySectorView(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    sectorCollection = dbconn['clnSectors']

    if request.method == 'POST':
        #get our collection
        docs_list  = list(sectorCollection.find())
        return Response(json.dumps(docs_list, default=json_util.default))
    else:    
        return Response("failure")


#created by Arun.R.Menon
#on 13-10-14
@csrf_exempt
@api_view(['GET','POST'])
def CountryStateDistrictView(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    CountryStateDistrictCollection = dbconn['clnCountryStateDistrict']

    if request.method == 'POST':
        #get our collection
        
        docs_list  = list(CountryStateDistrictCollection.find())
        return Response(json.dumps(docs_list, default=json_util.default))
    else:    
        return Response("failure")

#created by Suhail Pallimalil
#on 13-10-14
@csrf_exempt  
@api_view(['GET','POST'])
def Login(request):
    #connect to our local mongodb
        db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
        #get a connection to our database
        dbconn = db[settings.MONGO_DB]
        userLoginCollection = dbconn['clnUserLogin']
        if request.method == 'POST':
            stream =StringIO(request.body)
            data = JSONParser().parse(stream)            
            try:
                log = dbconn.system_js.fnLogin(data);
            except:
                return Response("error")
            return Response(json.dumps(log, default=json_util.default))
        else:    
            return Response("failure")    
#created by MIDHUN SUDHAKAR
#on 10-10-14
@csrf_exempt  
@api_view(['GET','POST'])
def ManageRolesOfCompany(request): #this webservice add roles of particular company
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)    #get a connection to our database
    dbconn =db[settings.MONGO_DB]
    if request.method == 'POST':
        #docs_list  = list(userMenuCollection.find({"fkRoleId":ObjectId("542d498fcf19c1514235f69d")}))
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        roles=data['roles']
        try:
            dbconn.system_js.fun_add_new_roles(roles);
        except:
            return Response(json.dumps("error", default=json_util.default))
        return Response(json.dumps("success", default=json_util.default))
    else:
        return Response(json.dumps("failed", default=json_util.default))  
#created by MIDHUN SUDHAKAR
#on 12-10-14

@csrf_exempt
@api_view(['GET','POST'])
def ManageRolesOfCompanyView(request):  #this service will retrieve all roles of particular company
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]

    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        cmpid=data["companyId"]
        try:
            rolls=dbconn.system_js.function_retriveCompany_Roles(cmpid)    
        except:
            return Response(json.dumps("error", default=json_util.default))
        # return Response(json.dumps(rolls, default=json_util.default))
        return Response(json.dumps(rolls, default=json_util.default))
    else:        
        return Response(json.dumps("failed", default=json_util.default))
#created by MIDHUN SUDHAKAR
#on 16-10-14

@csrf_exempt
@api_view(['GET','POST'])
def UpdateCompanyRole(request):  #this service will update all roles of particular company
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        RoleId=data["_id"]
        role=data["role"]
        data=data["data"]
        try:
            dbconn.system_js.fun_update_company_role(RoleId,role,data)
        except:
            return Response(json.dumps("error", default=json_util.default))
        return Response(json.dumps("success", default=json_util.default))
    else:
         return Response(json.dumps("failed", default=json_util.default)) 


#created by MIDHUN SUDHAKAR
#on 16-10-14

@csrf_exempt
@api_view(['GET','POST'])
def DeleteCompanyRole(request):  #this service will change active flag of role of a particular company
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    CompanyRoles = dbconn['ClnRoleMaster']  #ClnRoleMaster is the collection that stores roles

    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        RoleId=data["_id"]
        try:
            dbconn.system_js.fun_delete_company_role(RoleId)    
        except:
            return Response(json.dumps("error", default=json_util.default))
        return Response(json.dumps("success", default=json_util.default))
    else:        
        return Response(json.dumps("failed", default=json_util.default))

#created by Arun.R.Menon
#to delete a company
@csrf_exempt
@api_view(['GET','POST'])
def CompanyDeleteView(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]

    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        dbconn.system_js.fnDeleteCompany(data);
        return Response("success")
    else:    
        return Response("failure")

#created by Arun.R.Menon
#to delete a company
@csrf_exempt
@api_view(['GET','POST'])
def CompanyEditView(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    companyCollection = dbconn['clnCompany']

    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        dbconn.system_js.fnEditCompany(data);
        return Response("success")
    else:    
        return Response("failure")


#created by Arun.R.Menon
#on 13-10-14
@csrf_exempt
@api_view(['GET','POST'])
def UserNameValidView(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    UserLoginCollection = dbconn['clnUserLogin']

    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        result = dbconn.system_js.fnUserNameValid(data);
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")

#created by midhun
#on 22-10-14
# @csrf_exempt
# @api_view(['GET','POST'])
# def show_more_company_role(request):  #this service will change active flag of role of a particular company
#     #connect to our local mongodb
#     db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
#     #get a connection to our database
#     dbconn = db[settings.MONGO_DB]
    
#     if request.method == 'POST':
#         stream = StringIO(request.body)
#         data = JSONParser().parse(stream) 
#         showtime=data["showtime"]
#         companyId=data["companyId"]       
#         try:
#             maore_roles=dbconn.system_js.fn_show_more_roles(companyId,showtime)
#         except:
#             return Response("error")
#         return Response(json.dumps(maore_roles, default=json_util.default))
#     else:
#         return Response("failed")
        
#---------------------------------------------------------------------
#created by  : Akshath kumar M.
#created date: 24-10-14
#Description : getting the user details for reporting.   
#---------------------------------------------------------------------      
@csrf_exempt
@api_view(['GET','POST'])
def getRptUserDetails(request):  #this service will change active flag of role of a particular company
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    
    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream) 
        userRoleMappingId=data["userRoleMappingId"]       
        try:
            role=dbconn.system_js.fnGetRptUserDetails(userRoleMappingId)
        except:
            return Response("error")
        return Response(json.dumps(role, default=json_util.default))

#created by Arun
#on 22-10-14
@csrf_exempt
@api_view(['GET','POST'])
def showMoreCompaniesView(request):  #this service will change active flag of role of a particular company
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    
    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream) 
        showtime=data["showtime"]       
        try:
            company=dbconn.system_js.fnShowMoreCompany(showtime)
        except:
            return Response("error")
        return Response(json.dumps(company, default=json_util.default))
    else:        
        return Response("failure")

#created by midhun
#on 22-10-14
# @csrf_exempt
# @api_view(['GET','POST'])
# def find_company_id(request):  #this service will find the company id of current session
#     #connect to our local mongodb
#     db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
#     #get a connection to our database
#     dbconn = db[settings.MONGO_DB]
    
#     if request.method == 'POST':
#         stream = StringIO(request.body)
#         data = JSONParser().parse(stream) 
#         fkUserLoginId=data["fkUserLoginId"]
#         try:
#             role=dbconn.system_js.fun_companyid_mappings(fkUserLoginId)
#             cmpid=role.get('fkCompanyId')
#         except:
#             return Response("error")
#         return Response(json.dumps(cmpid, default=json_util.default))
#     else:        
#         return Response("failed")
#created by suhail pallimalil
#on 22-10-14
@csrf_exempt
@api_view(['GET','POST'])
def EmailAlreadyRegisterdorNot(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    UserLoginCollection = dbconn['clnUserLogin']

    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        result = dbconn.system_js.fnCheckEmailExist(data['email'],data['fbId']);
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")

@csrf_exempt
@api_view(['GET','POST'])
def LinkAccountWithFacebook(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    UserLoginCollection = dbconn['clnUserLogin']

    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        result = dbconn.system_js.fnLinkwithFacebook(data);
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")        


#created by Arun.R.Menon
#on 13-10-14
@csrf_exempt
@api_view(['GET','POST'])
def SelectedCompanyView(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    
    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        result = dbconn.system_js.fnSelectedCompany(data);
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")   

#created by Arun.R.Menon
#on 13-10-14
@csrf_exempt
@api_view(['GET','POST'])
def SearchCompanyView(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    
    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        result = dbconn.system_js.fnSearchCompany(data);
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")   

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
        result = dbconn.system_js.fnUserNameValid(data);
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")

#service for ckecking  company name already exists or not
#Author: Akshath kumar M.
@csrf_exempt
@api_view(['GET','POST'])    
def FnCheckCompanyNameExists(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
   
    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        result = dbconn.system_js.fnCheckCompanyNameValid(data);
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")

#service for inserting compan signup details
#Author: Akshath kumar M.        
@csrf_exempt
@api_view(['GET','POST'])
def FnCompanySignup(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    
    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        result = dbconn.system_js.fnCompanySignup(data['companyName'],data['userName'],data['password'])
        email= data['userName']
        email = EmailMessage('Company Registered','Welcome to SocialBee, Now you can login to your account using your credentials', to=[email])
        email.send()
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")

#created by Akshath kumar M
#Service for loading company sectors
@csrf_exempt
@api_view(['GET','POST'])
def FnLoadCompanySectors(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    sectorCollection = dbconn['clnSectors']

    if request.method == 'POST':
        #get our collection
        docs_list  = list(sectorCollection.find())
        return Response(json.dumps(docs_list, default=json_util.default))
    else:    
        return Response("failure")

#created by Arun.R.Menon
#on 13-10-14
@csrf_exempt
@api_view(['GET','POST'])
def FnLoadCountryStateDistrict(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    CountryStateDistrictCollection = dbconn['clnCountryStateDistrict']

    if request.method == 'POST':
        #get our collection
        
        docs_list  = list(CountryStateDistrictCollection.find())
        return Response(json.dumps(docs_list, default=json_util.default))
    else:    
        return Response("failure")

##created by Akshath kumar M.
#Description: Service fuction for updating company signup details.
@csrf_exempt
@api_view(['GET','POST'])
def FnUpdateCompanySignupDetails(request):
    #connect to our local mongodb
    db = Connection(settings.MONGO_SERVER_ADDR,settings.MONGO_PORT)
    #get a connection to our database
    dbconn = db[settings.MONGO_DB]
    #companyCollection = dbconn['clnCompany']

    if request.method == 'POST':
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        try:
            companyList=dbconn.system_js.FnUpdateCompanySignupDetails(data["companyId"],data['urmId'],data['data'])
        except:
            return Response(data)
        return Response(json.dumps(companyList, default=json_util.default))
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
        result = list(clnSocialConfigDetails.find({'fkUserId':str(data['urmId']),'fkWebsiteId':str(data['websiteId'])}));
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
        extension = file_obj.content_type.split('/')[0]
        result = dbconn.system_js.FnSaveSocialConfigDetails(data);

        filename=result.get('pic')
        if(default_storage.exists(settings.FILEUPLOAD_PATH+'/socialConfigImages/'+str(filename))):
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
#         page_token='CAACEdEose0cBAE7zjo5m0fTDONbgLmAB6kMPrMZC1pn3U4TzQD7pQlazUz7yXA9C0BrHKirWOb5ZAbh7XRcViao7ZCvPKJJsRKHxen0jInVw6kvVZBeiAOFfIgLmTi0FiYb2St76c8pV2olM2cIZBohlxpt2y8QEK8yj4NZBFAFKvYz8PRdKeS42kxkBDq9PYXpdRI1p9CqUytRVmPn7BZC'
#         access_token_page='CAACEdEose0cBAKXIpivWvKqfnfRKK0HsRIAfBIeD9yMTAolkvd5zq5QCJpYPjg0megyNfcPDFYjUgCAnCmJ8ZBZBXcyIMd25FepNGvlOUJOiZBghTgfl6xNbsk7Ipa7s0vZBCTWa3ZBes1T7A95CSKdswL1LGI5IAXfhcbD3nY2ZBEQD4S4PU1sBdDEvdi9tZBNiXLn2m1bDZCHY0VqxpLgS'
#         FACEBOOK_APP_ID = '610577519050579'
#         FACEBOOK_APP_SECRET = '281797352ce378d168bc40ce9afe3c2c'
#         FACEBOOK_PROFILE_ID = '100006914924908'

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
        result = list(clnSocialConfigDetails.find());
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
    clnSocialConfigDetails = dbconn['clnChannels']
    #return Response({"companyId":companyId,"name":name}) 
    if request.method == 'POST':      
        stream = StringIO(request.body)
        data = JSONParser().parse(stream)
        result =  dbconn.system_js.fnGetBroadcastTypeTemplate(data['channelId'],data['broadcastTypeId'])
        return Response(json.dumps(result, default=json_util.default))            
    else:        
        return Response("failure")  