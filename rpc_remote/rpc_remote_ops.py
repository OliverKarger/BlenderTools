import bpy

from ..networking import socket, xmlrpc

class BlenderTools_RpcRemoteCheckAddress(bpy.types.Operator):
    bl_idname = "blendertools.rpcremote_checkaddress"
    bl_label = "Check Server"

    def execute(self, context):
        props = context.scene.blendertools_rpcremote

        if not props.port and not props.ip:
            self.report({ "ERROR" }, "Please input both IP and Port!")
            return { "CANCELLED" }

        if int(props.port) < 10000:
            self.report({ "ERROR" }, "Port must be larger than 10000!")
            return { "CANCELLED" }

        is_used = socket.check_connection(props.ip, int(props.port))
        if is_used:
            self.report({"ERROR"}, "IP and/or Port is already in use by some Service!")
            return { "CANCELLED" }

        self.report({ "INFO" }, "IP and Port are looking good!")
        return { "FINISHED" }
    
class BlenderTools_RpcRemoteStartServer(bpy.types.Operator):
    bl_idname = "blendertools.rpcremote_startserver"
    bl_label = "Start Server"

    def execute(self, context):
        props = context.scene.blendertools_rpcremote
        props.is_active = True

        xmlrpc.stop_event.set()
        xmlrpc.server_instance = None
        
        xmlrpc.server_instance = xmlrpc.XmlRpcServer(props.ip, int(props.port))
        xmlrpc.server_instance.start()
        return { "FINISHED" }
    
class BlenderTools_RpcRemoteStopServer(bpy.types.Operator):
    bl_idname = "blendertools.rpcremote_stopserver"
    bl_label = "Stop Server"

    def execute(self, context):
        props = context.scene.blendertools_rpcremote
        props.is_active = False
        xmlrpc.stop_event.set()
        return { "FINISHED" }

def register():
    bpy.utils.register_class(BlenderTools_RpcRemoteCheckAddress)
    bpy.utils.register_class(BlenderTools_RpcRemoteStartServer)
    bpy.utils.register_class(BlenderTools_RpcRemoteStopServer)

def unregister():
    bpy.utils.unregister_class(BlenderTools_RpcRemoteCheckAddress)
    bpy.utils.unregister_class(BlenderTools_RpcRemoteStartServer)
    bpy.utils.unregister_class(BlenderTools_RpcRemoteStopServer)