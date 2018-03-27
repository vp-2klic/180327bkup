import SocketServer
import logging

import django_setup_env

from acwebif.models import MyLog
from django.utils import timezone

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S',
                   )

class DevicesTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        logging.debug("TCP {} received: %s".format(self.client_address[0]) %data)
        if "LOG" in data:
            mylog = MyLog(log_text=data, log_date=timezone.now())
            mylog.save()
            logging.debug("Updated log to database with data: %s" %mylog.log_text)
#            logging.debug("Updated database")
        else:
            logging.debug("NOT update database")

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    import threading
    import time

    server_addr = ('192.168.0.6', 8080)
    tcpserver = ThreadedTCPServer(server_addr, DevicesTCPRequestHandler)
    tcpserver.allow_reuse_address = True
    tcpserver_thr = threading.Thread(target=tcpserver.serve_forever)
    tcpserver_thr.setDaemon(True)
    tcpserver_thr.start()
    logging.debug("Start TCP Server")

while True:
    time.sleep(1)

