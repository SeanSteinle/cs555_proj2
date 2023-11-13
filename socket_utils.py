import socket

def create_socket(router_id: int):
    host, port = socket.gethostname(), 50000+router_id
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    return s

def signal_router(s: socket.socket, msg: str):
    s.sendall(bytes(msg, "utf-8"))
    response = s.recv(1024)
    return response
