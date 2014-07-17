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
            self.request.sendall(bytes(json.dumps(wrapper.command(test)), 'UTF-8'))
        except Exception as e:
            print("Exception wile receiving message: ", e)


class TS3Wrapper():
    def __init__(self):
        self.server = TS3Server(ts3address, ts3port)
        self.server.login(ts3admin_user, ts3admin_pass)
        self.server.use(1)

    def command(self, command):
        commands = {
            "clients": self.clients,
            "channels": self.channels,
            "virtual_servers": self.virtual_servers,
            "vote_kick": self.vote_kick,
        }

        return commands[command["command"]](command)

    def clients(self, command):
        clients_raw = self.server.clientlist()
        clients = [Client(**clients_raw[client]) for client in clients_raw]

        return Client.clients_json(clients)

    def channels(self, command):
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
        virtual_servers_raw = self.server.serverlist().data
        virtual_servers = [VirtualServer(**vs) for vs in virtual_servers_raw]

        # TODO Only return data about the first virutal server, need to research adding additional virtual servers
        return VirtualServer.virtual_server_json(virtual_servers[0])

    def vote_kick(self, command):

        self.server.send_command(
            'clientkick',
            keys={
                "clid": command["clid"],
                "reasonid": 5,
                "reasonmsg": "Vote Kick"
            }
        )

        return {'return':'ok', 'command':'vote_kick'}


wrapper = TS3Wrapper()


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

"""

