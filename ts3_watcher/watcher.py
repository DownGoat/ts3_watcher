"""
The MIT License (MIT)

Copyright (c) <year> <copyright holders>

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
from ts3_watcher.models.server import Server
from ts3_watcher.models.virtual_server import VirtualServer
from ts3_watcher.models.vote_kick import VoteKick
from ts3_watcher.config import ts3address, ts3admin_pass, ts3admin_user, ts3port
from ts3_watcher.database import db_session


def run():
    server = TS3Server(ts3address, ts3port)
    server.login(ts3admin_user, ts3admin_pass)

    virtual_servers_raw = server.serverlist().data
    print(virtual_servers_raw)
    virtual_servers = [VirtualServer(**vs) for vs in virtual_servers_raw]

    for virtual_server in virtual_servers:
        db_session.add(virtual_server)

    db_session.commit()

    server.use(1)

    channels_raw = server.send_command("channellist").data
    print(channels_raw)
    channels = [Channel(**channel) for channel in channels_raw]

    clients_raw = server.clientlist()
    print(clients_raw)
    clients = [Client(**clients_raw[client]) for client in clients_raw]

    print("bp")