from jsonrpclib import Server
import threading
import argparse
import socket

class RPCCommError(Exception):
    pass

class RPCClient(Server):

    functions = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._server = Server("http://{}:{}".format(self.host, self.port))
        #self.retrieve_function_list()

    def wrapper(self, func):
        return RPCFunction(func)

    def retrieve_function_list(self):
        try:
            self.functions = self.__getattr__("list_functions")()
        except RPCCommError:
            self.functions = None

    def __getattr__(self, attr_name):
        #print("Getting attribute {}".format(attr_name))
        try:
            attr = self._server.__getattr__(attr_name)
        except socket.error as e:
            if e.errno == 111:
                error = RPCCommError("Connection refused")
                error.errno = e.errno
                raise error
        return self.wrapper(attr)

class RPCFunction(object):
    def __init__(self, func):
        self.func = func

    def __eq__(self, other):
        return False

    def __call__(self, *args, **kwargs):
        try:
            return self.func(*args, **kwargs)
        except socket.error as e:
            if e.errno == 111:
                error = RPCCommError("Connection refused")
                error.errno = e.errno
                raise error

api = RPCClient("127.0.0.1", 9376)

def main():
    parser = argparse.ArgumentParser(prog='zp', description='ZeroPhone API CLI')
    commands = api.list_functions()
    parser.add_argument('action', action="store")
    parser.add_argument('params', nargs='*', default=[])
    args = parser.parse_args()
    try:
        result = getattr(api, args.action)(*args.params)
    except:
        print(api.get_help(args.action))
    else:
        print(result)

if __name__ == "__main__":
    main()
