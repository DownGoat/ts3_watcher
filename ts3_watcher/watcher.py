"""
The MIT License (MIT)

Copyright (c) <2014> <Sindre Smistad>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
__author__ = 'Sindre Smistad'


from ts3 import TS3Server
from ts3_watcher.models.channel import Channel
from ts3_watcher.models.client import Client
from ts3_watcher.models.virtual_server import VirtualServer
from ts3_watcher.config import ts3address, ts3admin_pass, ts3admin_user, ts3port
import socketserver
import json


class MyTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

class MyTCPServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        """
        This class is used to handle the socket stuff, it accepts incoming connections and reads the received data.
         The data is then sent elsewhere for processing, and it replies with the returned data.

        """
        try:
            data = self.request.recv(1024).decode('UTF-8').strip()
            # process the data, i.e. print it:

            test = json.loads(data)

            # send some 'ok' back

            #channels_raw = server.send_command("channellist").data
            #channels = [Channel(**channel) for channel in channels_raw]

            #clients_raw = server.clientlist()
            #clients = [Client(**clients_raw[client]) for client in clients_raw]
            #test = Client.clients_json(clients)
            self.request.sendall(bytes(json.dumps(handler.command(test)), 'UTF-8'))
        except Exception as e:
            print("Exception wile receiving message: ", e)


class CommandHandler():
    """
    This is class is responsible for processing the received commands, and carry out the commands.
    The class receives commands, process them, executes them and sends back the result.
    """
    def __init__(self):
        self.server = TS3Server(ts3address, ts3port)
        assert self.server._connected
        assert self.server.login(ts3admin_user, ts3admin_pass)
        assert self.server.use(1)


    def command(self, command):
        """
        This method is responsible for processing the command and calling the method that will execute the command.

        @param command: The received command that is parsed JSON, the method expects a dict object.
        @return: The method returns what is returned from the method executing the command.
        """

        # This is a serves as a switch statement, looks better than a lot of if elses
        commands = {
            "clients": self.clients,
            "channels": self.channels,
            "virtual_servers": self.virtual_servers,
            "vote_kick": self.vote_kick,
        }

        # TODO this will crash if the command is not found HANDLE IT!
        # A bit confusing, but it uses the command from the input to call the right method, and passes the input to the
        # method.
        try:
            return commands[command["command"]](command)
        except KeyError as error:
            return {"return": "error", "msg": "Command not found."}

    def clients(self, command):
        """
        This method gets a list of the clients currently connected to the server.

        @param command: The command dict
        @return: Returns a JSON list of all the clients, and information about the clients.
        """
        clients_raw = self.server.clientlist()
        clients = [Client(**clients_raw[client]) for client in clients_raw]

        return Client.clients_json(clients)

    def channels(self, command):
        """
        This method gets a list of the channels, the data includes all the information about the channels, and the
        clients currently in the channel.

        @param command: The command dict
        @return: Returns a JSON list of the channels with clients and all the information about the channel and clients.
        """
        channels_raw = self.server.send_command("channellist").data
        channels = [Channel(**channel) for channel in channels_raw]

        clients_raw = self.server.clientlist()
        clients = [Client(**clients_raw[client]) for client in clients_raw]

        for client in clients:
            for channel in channels:
                if client.cid == channel.cid:
                    channel.clients.append(client)


        return Channel.channels_json(channels)

    def virtual_servers(self, command):
        """
        This method returns information about the first virtual server in the list returned from the TS query interface.

        @param command: The command dict
        @return: Returns a JSON object of the virtual server containing all the information about the server.
        """
        virtual_servers_raw = self.server.serverlist().data
        virtual_servers = [VirtualServer(**vs) for vs in virtual_servers_raw]

        # TODO Only return data about the first virutal server, need to research adding additional virtual servers
        return VirtualServer.virtual_server_json(virtual_servers[0])


    def vote_kick(self, command):
        """
        This method kicks a client from the server,
        @param command: The command dict, the dict need a parameter named clid which has to be the id of the client to
        kick.

        @return: Returns a status message about the results of the execution of the command.

        """
        self.server.send_command(
            'clientkick',
            keys={
                "clid": command["clid"],
                "reasonid": 5,
                "reasonmsg": "Vote Kick"
            }
        )

        return {'return':'ok', 'command':'vote_kick'}


handler = CommandHandler()


def run():
    #virtual_servers_raw = server.serverlist().data
    #virtual_servers = [VirtualServer(**vs) for vs in virtual_servers_raw]

    #for virtual_server in virtual_servers:
    #    db_session.add(virtual_server)

    #db_session.commit()

    #server.use(1)

    sock_server = MyTCPServer(('127.0.0.1', 13373), MyTCPServerHandler)
    sock_server.serve_forever()

"""
{
   "command":"clients",
   "test":123.4
}

{
   "command":"channels",
   "test":123.4
}

{
   "command":"virtual_servers",
   "test":123.4
}

{
   "command":"vote_kick",
   "clid":1
}

{
   "command":"foobar",
   "clid":1
}

"""

