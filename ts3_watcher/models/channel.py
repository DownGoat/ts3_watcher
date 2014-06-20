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
from ts3_watcher.models.client import Client
from ts3_watcher.database import Model
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey


__author__ = 'Sindre Smistad'


class Channel(Model):

    __tablename__ = "channel"
    id = Column('id', Integer, primary_key=True)
    channel_order = Column(Integer)
    cid = Column(Integer)
    pid = Column(Integer)
    channel_name = Column(String(2048))
    clients = Column(Integer)
    channel_description = Column(String(2048))


    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if v is None:
                v = 0
            setattr(self, k, v)

        self.clients = []


    @staticmethod
    def channel_json(channel):
        return {
            "channel_order": channel.channel_order,
            "cid": channel.cid,
            "pid": channel.pid,
            "channel_name": channel.channel_name,
            "clients": Client.clients_json(channel.clients),
            "channel_description": channel.channel_description
        }

    @staticmethod
    def channels_json(channels):
        return [Channel.channel_json(channel) for channel in channels]

    def __str__(self):
        return str(Channel.channel_json(self))

    def __repr__(self):
        return self.__str__()

