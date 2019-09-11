#!/use/bin/env python
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#重用地址
localhost = '127.0.0.1'
addr = (localhost, 8000)
sock.bind(addr)
sock.listen(50)

# 接收缓冲区为1024
msg="""
http/1.1 200 OK

<html>
<head><title>myweb</title>
</head>
<body>yes
</body>
</html>
"""
while 1:
    cli_sock, cli_addr = sock.accept()
    cli_data = cli_sock.recv(1024)
    cli_sock.sendall(msg.encode('utf-8'))
    if 0:
        break
time.sleep(1)
cli_sock.close()
