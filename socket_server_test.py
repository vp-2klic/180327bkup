import SocketServer
import logging

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(levelname)s (%(threadName)-2s) %(message)s',
#                     )

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S',
                    )

def getIP():
    tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tmp.connect(('8.8.8.8', 80))
    ip = tmp.getsockname()[0]
    tmp.close()
    return ip

def door_open_request(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(addr)
    logging.debug("Sending Request Open Door...")
    try:
        sock.send("DR00OPEN")
        response = sock.recv(100)
        if "OK" in response:
            logging.debug("Request Open Door Success")
        else:
            logging.debug("Request Open Door Fail")
    finally:
        sock.close()

class DevicesTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        logging.debug("TCP {} received: %s".format(self.client_address[0]) %data)
        if "UID=" in data:
            uid_tag = data[data.index("=")+1: data.index("=")+9]
            if uid_tag in allow_tags:
                self.request.send("UID.PASS")
                logging.debug("Tag with UID = %s authenticated" % uid_tag)
                door_open_request(door_addr)
            else:
                self.request.send("UID.FAIL")
                logging.debug("Tag with UID = %s unauthenticated" % uid_tag)

class DevicesUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        [data, socket] = self.request
#        socket = self.request[1]
        logging.debug("UDP {} wrote: %s".format(self.client_address[0]) % data)
#        print "socket: ", socket
        if "id00" in data:
            socket.sendto(data.upper(), self.client_address)
            logging.debug("Sent: {}".format(data.upper()))
        else:
            socket.sendto("NOT Auth", self.client_address)
            logging.debug("Sent refuse")

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    import threading
    import socket
    import time
    
#    udp_addr = ('', 5000)
#    udpserver = SocketServer.UDPServer(udp_addr, DevicesUDPRequestHandler)
#    logging.debug("Start UDP server")
#    udpserver.serve_forever()
    
#    tcp_addr = ('192.168.0.6', 8000)
#    tcpserver = SocketServer.TCPServer(tcp_addr, DevicesTCPRequestHandler)
#    logging.debug("Start TCP server")
#    tcpserver.serve_forever()
    test_ip = getIP()
    door_addr = ('192.168.0.15', 8000)

    print test_ip
    allow_tags = ['0a86c26f', '97e8340c']

    udp_addr = ('', 5000)
    udpserver = ThreadedUDPServer(udp_addr, DevicesUDPRequestHandler)
    udpserver_thr = threading.Thread(target=udpserver.serve_forever)
    udpserver_thr.setDaemon(True)
    udpserver_thr.start()
    logging.debug("Start UDP server")

    tcp_addr = (test_ip, 8000)
    tcpserver = ThreadedTCPServer(tcp_addr, DevicesTCPRequestHandler)
    tcpserver_thr = threading.Thread(target=tcpserver.serve_forever)
    tcpserver_thr.setDaemon(True)
    tcpserver_thr.start()
    logging.debug("Start TCP server")

while True:
    time.sleep(1)
