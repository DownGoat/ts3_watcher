"""
The MIT License (MIT)

Copyright (c) 2014 Sindre Knudsen Smistad

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
from ts3_watcher.models.channel import Channel

__author__ = 'Sindre Smistad'


class VirtualServer():
    """
    {
        'virtualserver_status': 'online',
        'virtualserver_uptime': '25905',
        'virtualserver_machine_id': None,
        'virtualserver_maxclients': '32',
        'virtualserver_port': '9987',
        'virtualserver_clientsonline': '1',
        'virtualserver_queryclientsonline': '0',
        'virtualserver_autostart': '1',
        'virtualserver_id': '1',
        'virtualserver_name': 'TeamSpeak ]I[ Server'
    }
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if v is None:
                v = 0
            setattr(self, k, v)

        self.channels = []

    @staticmethod
    def virtual_server_json(server):
        return {
            "virtualserver_id": server.virtualserver_id,
            "virtualserver_name": server.virtualserver_name,
            "virtualserver_clientsonline": server.virtualserver_clientsonline,
            "virtualserver_port": server.virtualserver_port,
            "virtualserver_uptime": server.virtualserver_uptime,
            "virtualserver_status": server.virtualserver_status,
            "virtualserver_maxclients": server.virtualserver_maxclients,
            "virtualserver_machine_id": server.virtualserver_machine_id,
            "virtualserver_queryclientsonline": server.virtualserver_queryclientsonline,
            "virtualserver_autostart": server.virtualserver_autostart,
            "channels": Channel.channels_json(server.channels),
        }

    def __str__(self):
        return str(VirtualServer.virtual_server_json(self))

    def __repr__(self):
        return self.__str__()