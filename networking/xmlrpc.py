import threading
import xmlrpc.server as xmlrpcserver

stop_event = threading.Event()

server_instance = None


class XmlRpcServer:
    def __init__(self, ip: str, port: int):
        self.server = xmlrpcserver.SimpleXMLRPCServer((ip, port), allow_none=True, logRequests=True)
        self.thread = threading.Thread(target=self.__serve, daemon=True)

    def start(self):
        self.thread.start()
        print("Started Xml Rpc Server!")
        pass

    def __serve(self):
        while not stop_event.is_set():
            print("Awaiting Requests")
            self.server.handle_request()
        print("Stopped Xml Rpc Server")
