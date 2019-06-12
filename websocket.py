from websocket_server import WebsocketServer
from model import Model
import json
import datetime

model = Model()

# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
   #server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message_data):
    try:
        print(message_data)
        message_data = json.loads(message_data)
        # check required parament
        message_data["access_token"]
        message_data["chatroom_secret"]
        message_data["message"]
        now = datetime.datetime.now()
        user_name = model.insert_message_to_chatroom_db(message_data["access_token"], message_data["chatroom_secret"], message_data["message"], now)
        if user_name != None:
            print("Client(%d) said: %s" % (client['id'], message_data))
            data = { 
                "name" : user_name, 
                "message" : message_data["message"], 
                "chatroom_secret" : message_data["chatroom_secret"],
                "timestamp" : now.isoformat()
            }
            server.send_message_to_all(json.dumps(data, ensure_ascii=False))
        else:
            print("insert message to db error")
    except KeyError as e:
        print("KeyError, maybe missing parameter: " + e.args[0])
    except Exception as e:
        print(e)
        print("[error] Client(%d) said: %s" % (client['id'], message_data))
    


PORT=9500
server = WebsocketServer(PORT, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
