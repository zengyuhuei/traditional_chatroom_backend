import json
from config.Config import Config as config
from db import DB
import facebook
import uuid
import datetime
from pytz import timezone
class Model:
    def __init__(self):
        self._con = config()
        self._traditional_chatroom_db = DB("traditional_chatroom").connect()
        self._account_table = self._traditional_chatroom_db["account"]
        self._chatroom_table = self._traditional_chatroom_db["chatroom"]
        self._message_table = self._traditional_chatroom_db["message"]

    def get_facebook_user_info(self, access_token):
        graph = facebook.GraphAPI(access_token=access_token, version="3.1")
        user = None
        try : 
            user = graph.get_object('me')
        except :
            pass
        print(user)
        return user

    def add_account(self, access_token):
        user = None
        result = None
        try :
            user = self.get_facebook_user_info(access_token)
        except :
            pass
        # if access token is valid
        if user!=None :
            account_data = {"facebook_id" : user["id"] , "name" : user["name"], "access_token" : access_token}
            # upsert : insert if not exist / update if exist
            result = self._account_table.update_one({'facebook_id':user["id"]}, {"$set": account_data}, upsert=True)
        return result 

    def get_user_by_token(self, access_token):
        user = None
        result = None
        try :
            user = self.get_facebook_user_info(access_token)
        except :
            pass
        # if access token is valid
        if user!=None :
            result = self._account_table.find_one({'facebook_id':user["id"]}, {"_id": 0})
        return result 

    def add_chatroom(self, access_token, chatroom_name, chatroom_image_base64):
        user = None
        result = None
        try :
            user = self.get_facebook_user_info(access_token)
            print(user)
        except :
            pass
        # if access token is valid
        if user!=None :
            chatroom_secret = str(uuid.uuid1())
            chatroom_data = {"chatroom_name" : chatroom_name, "chatroom_image_base64" : chatroom_image_base64, "chatroom_secret" : chatroom_secret}
            # upsert : insert if not exist / update if exist
            result = self._chatroom_table.insert_one(chatroom_data)
            return chatroom_secret
        return result 

    def get_chatroominfo_by_secret(self, chatroom_secret):
        result = None
        result = self._chatroom_table.find_one({'chatroom_secret': chatroom_secret}, {"_id": 0})
        return result 

    def insert_message_to_chatroom_db(self, access_token, chatroom_secret, message, timestamp):
        user = None
        chatroom = None
        result = None
        try :
            user = self.get_facebook_user_info(access_token)
            chatroom = self.get_chatroominfo_by_secret(chatroom_secret)
        except :
            pass
        # if access token is valid
        if user!=None and chatroom!=None:
            # connect db
            messge_to_db = {"facebook_id" : user["id"] , "name" : user["name"], "message" : message, "chatroom_secret":chatroom_secret, "timestamp": timestamp}
            self._message_table.insert_one(messge_to_db)
            result = user["name"]
        return result 

    def get_message_by_secret(self, chatroom_secret):
        result = None
        result = list(self._message_table.find({'chatroom_secret': chatroom_secret}, {"_id": 0, "facebook_id": 0}))
        for message in result:
            if type(message["timestamp"] == type(datetime.datetime.now())):
                message["timestamp"] = message["timestamp"].astimezone(timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        return result 
