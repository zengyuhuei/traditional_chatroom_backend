from flask import Flask, jsonify, request
from model import Model
from response import Response
import json

model = Model()


# init Flask 
app = Flask(__name__)
    
@app.route('/checkToken', methods=['GET'])
def check_token():
    response = Response()
    access_token = request.args.get('facebook_token')
    user = model.get_facebook_user_info(access_token)
    if user!=None :
        response.success()
        return response.get_json()
    else :
        response.error("invalid token")
        return response.get_json()

@app.route('/addAccount', methods=['GET'])
def add_account():
    response = Response()
    access_token = request.args.get('facebook_token')
    result = model.add_account(access_token)
    if result!=None :
        response.success()
        return response.get_json()
    else :
        response.error("invalid token")
        return response.get_json()

@app.route('/addChatroom', methods=['POST'])
def add_chatroom():
    response = Response()
    try:
        
        add_data = request.get_json()

        # check required parament
        add_data["access_token"]
        add_data["chatroom_name"]
        add_data["chatroom_image_base64"]
        
        result = model.add_chatroom(add_data["access_token"], add_data["chatroom_name"], add_data["chatroom_image_base64"])
        if result == None:
            raise Exception(result)
        response.success(result)

    except KeyError as e:
        response.error("KeyError, maybe missing parameter: " + e.args[0])

    except Exception as e:
        response.error(str(e))

    return response.get_json()


@app.route('/getChatroomInfo', methods=['GET'])
def get_chatroom_info():
    response = Response()
    chatroom_secret = request.args.get('chatroom_secret')
    chatroom = model.get_chatroominfo_by_secret(chatroom_secret)
    if chatroom!=None :
        response.success(chatroom)
        return response.get_json()
    else :
        response.error("invalid chatroom_secret")
        return response.get_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9600, debug=True)

