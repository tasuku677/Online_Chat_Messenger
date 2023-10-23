import socket
import re


# ChatRoom クラス
class ChatRoom:
   def __init__(self, title, max_participants):
       self.title = title
       self.max_participants = max_participants
       self.participants = {}


# ChatClient クラス
class ChatClient:
   def __init__(self, client_address, port):
       self.client_address = client_address
       self.port = port
       self.additional_data = ""


# サーバーソケットを作成
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 9000))
server_socket.listen(1000)


# チャットルームを管理する辞書
chat_rooms = {}
#udp kanri dict
udp_socket = {}
# クライアントの接続を待ち受けるメインループ
port = 9051
while True:
   tcp_socket, client_addresses = server_socket.accept()
   print(client_addresses)
   try:
       # クライアントが新しいチャットルームを作成するリクエストか、参加するリクエストかを判断
       request = tcp_socket.recv(4096).decode()
       print(request)


       if request.startswith("CREATE_ROOM"):
           _, room_name, max_participants = request.split(':')
           max_participants = int(max_participants)
           chat_rooms[room_name] = ChatRoom(room_name, max_participants)
           chat_rooms[room_name].participants[client_addresses[0] + ':' + str(client_addresses[1])] = ChatClient(client_addresses[0], client_addresses[1])
           tcp_socket.send(f"room was created. client_address and port is {client_addresses}".encode())
           print("room was created successfully")
           # UDPで接続
           udp_socket[client_addresses[0] + ':' + str(client_addresses[1])] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
           udp_socket[client_addresses[0] + ':' + str(client_addresses[1])].bind(("0.0.0.0", port))  # クライアントのIPアドレス、ランダムなポート番号
           port += 1
           udp_socket[client_addresses[0] + ':' + str(client_addresses[1])].sendto(f"{client_addresses} and server were connected by UDP socket".encode(), client_addresses)
           print(f"{room_name}:", chat_rooms[room_name].participants.keys())
                  
       elif re.match(".+:join", request): #request is "join"
           room_name, _ = request.split(':')
           print(room_name)
           if room_name in chat_rooms:
               if len(chat_rooms[room_name].participants) < chat_rooms[room_name].max_participants:
                   chat_rooms[room_name].participants[client_addresses[0] + ':' + str(client_addresses[1])] = ChatClient(client_addresses[0], client_addresses[1])
                   tcp_socket.send("joined room successfully.".encode())
                   # UDPで接続
                   udp_socket[client_addresses[0] + ':' + str(client_addresses[1])] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                   udp_socket[client_addresses[0] + ':' + str(client_addresses[1])].bind(("0.0.0.0", port))  # クライアントのIPアドレス、ランダムなポート番号
                   port += 1
                   tcp_socket.send(f"UDP:{udp_socket[client_addresses[0] + ':' + str(client_addresses[1])].getsockname()[1]}".encode())
                   udp_socket[client_addresses[0] + ':' + str(client_addresses[1])].sendto(f"{client_addresses} and server were connected by UDP socket".encode(), client_addresses)
               else:
                   tcp_socket.send("room is full.".encode())
           else:
               tcp_socket.send("room not found.".encode())
           print(chat_rooms[room_name].participants)
       elif re.match(".+:\d+.*:.+", request): #request is message
           room_name, message_size, message = request.split(':')
           if room_name in chat_rooms:
               if client_addresses[0] + ":" + str(client_addresses[1]) in chat_rooms[room_name].participants:       
                   for participant in chat_rooms[room_name].participants.keys():
                       client_address, client_port = participant.split(':')
                       udp_socket[participant].sendto(message.encode(), (client_address, int(client_port)))
                       print("sending messages to participants")
                       udp_socket.close()
                   print("sent messages to all participants")
               else:
                   print("you are not a memmber of this room")
           else:
               print("you type in a wrong room name")
   except Exception as e:
       print("Error:" + str(e))
   finally:
       print("closing current connection")
       tcp_socket.close()
