import threading
import xmlrpc.server as xmlrpcserver

from .. import bt_logger
logger = bt_logger.get_logger(__name__)

stop_event = threading.Event()

server_instance = None

class XmlRpcServer:
    def __init__(self, ip: str, port: int):
        self.server = xmlrpcserver.SimpleXMLRPCServer((ip, port), allow_none=True, logRequests=True)
        self.thread = threading.Thread(target=self.__serve, daemon=True)

    def start(self):
        self.thread.start()
        logger.info(f"Started Xml Rpc Server at {self.ip}:{self.port}")
        print("Started Xml Rpc Server!")
        pass

    def __serve(self):
        while not stop_event.is_set():
            self.server.handle_request()
        logger.info("Stopped Xml Rpc Server")
