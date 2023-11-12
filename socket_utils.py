import socket

def signal_router(router_id: int):
    host, port = socket.gethostname(), 50000+router_id
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.sendall(b'share_table')
    response = s.recv(1024)
    s.close()
    return response