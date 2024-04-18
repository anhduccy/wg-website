import socket

def getIP():
    hostname = socket.gethostname()
    print(hostname)
    ip = socket.gethostbyname(hostname)
    print(ip)
    return ip