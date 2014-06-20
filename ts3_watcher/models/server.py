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
from ts3_watcher.database import Model
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey


__author__ = 'Sindre Smistad'


class Server(Model):

    __tablename__ = "server"
    id = Column('id', Integer, primary_key=True)
    server_name = Column(String(2048))
    status = Column(String(100))
    max_clients = Column(Integer)
    online_clients = Column(Integer)
    port = Column(Integer)
    uptime = Column(Integer)
    platform = Column(String(2048))
    welcome_message = Column(String(2048))


    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if v is None:
                v = 0
            setattr(self, k, v)


    @staticmethod
    def erver_json(server):
        return {
            "server_name": server.server_name,
            "status": server.status,
            "max_clients": server.max_clients,
            "online_clients": server.online_clients,
            "port": server.port,
            "uptime": server.uptime,
            "platform": server.platform,
            "welcome_message": server.welcome_message,
        }

    def __str__(self):
        return str(Server.server_json(self))

    def __repr__(self):
        return self.__str__()