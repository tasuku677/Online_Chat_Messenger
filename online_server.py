import socket
import threading
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
server_socket.listen(5)

# チャットルームを管理する辞書
chat_rooms = {}
# クライアントの接続を待ち受けるメインループ
port = 9050
while True:
    tcp_client_socket, client_addresses = server_socket.accept()
    try:
        # クライアントが新しいチャットルームを作成するリクエストか、参加するリクエストかを判断
        request = tcp_client_socket.recv(4096).decode()
        if request.startswith("CREATE_ROOM"):
            _, room_name, max_participants = request.split(':')
            max_participants = int(max_participants)
            chat_rooms[room_name] = ChatRoom(room_name, max_participants)
            chat_rooms[room_name].participants[client_addresses[0] + ':' + str(client_addresses[1])] = ChatClient(client_addresses[0], client_addresses[1])
            tcp_client_socket.send("room was created successfully.".encode())
            # UDPで接続
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.bind(('', 9001))  # クライアントのIPアドレス、ランダムなポート番号
            udp_socket.sendto(f"UDP:{udp_socket.getsockname()[1]}".encode(), client_addresses)
            udp_socket.close()
                    
        elif re.match(".+:join", request): #request is "join"
            _, room_name = request.split(':')
            if room_name in chat_rooms:
                if len(chat_rooms[room_name].participants) < chat_rooms[room_name].max_participants:
                    chat_rooms[room_name].participants[client_addresses[0] + ':' + str(client_addresses[1])] = ChatClient(client_addresses[0], client_addresses[1])
                    tcp_client_socket.send("joined room successfully.".encode())
                    tcp_client_socket.send(f"UDP:{udp_socket.getsockname()[1]}".encode())
                else:
                    tcp_client_socket.send("room is full.".encode())
            else:
                tcp_client_socket.send("room not found.".encode())
        elif re.match(".+:\d+.*:.+", request): #request is message
            room_name, message_size, message = request.split(':')
            if room_name in chat_rooms:
                if client_addresses[0] + ":" + str(client_addresses[1]) in chat_rooms[room_name].participants:        
                    for participant in chat_rooms[room_name].participants:
                        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        udp_socket.bind(('', 9003))
                        udp_socket.sendto(message.encode(), (participant.client_address, participant.port))
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
        print("Closing crrent connection")
        tcp_client_socket.close()

