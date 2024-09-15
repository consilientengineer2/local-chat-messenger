import socket
import os

# UNIXドメインソケットとデータグラム（非接続）ソケットを作成します
sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

# サーバのアドレスを定義します。
# サーバはこのアドレスでメッセージを待ち受けます
server_address = '/tmp/udp_socket_file'

# このクライアントのアドレスを定義します。
# サーバはこのアドレスにメッセージを返します
address = '/tmp/udp_client_socket_file'

input_message_type = input("message type (number) を入力してください。\n 1: name \n 2: address \n 3: text \n >>")

message_type_dict = {
    "1" : "name",
    "2" : "address",
    "3" : "text"
}

# サーバに送信するメッセージを定義します
message = message_type_dict.get(input_message_type, "-").encode("utf-8")

try:
    # もし前回の実行でソケットファイルが残っていた場合、そのファイルを削除します。
    os.unlink(address)
except FileNotFoundError:
    # ファイルが存在しない場合は何もしません。
    pass

# このクライアントのアドレスをソケットに紐付けます。
# これはUNIXドメインソケットの場合に限ります。
# このアドレスは、サーバによって送信元アドレスとして受け取られます。
sock.bind(address)

try:
    # サーバにメッセージを送信します
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, server_address)

    # サーバからの応答を待ち受けます
    print('waiting to receive')
    # 最大4096バイトのデータを受け取ります
    data, server = sock.recvfrom(4096)

    # サーバから受け取ったメッセージを表示します
    print('received {!r}'.format(data))

finally:
    # 最後にソケットを閉じてリソースを解放します
    print('closing socket')
    sock.close()