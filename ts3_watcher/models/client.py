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


__author__ = 'Sindre Smistad'


class Client():
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if v is None:
                v = 0
            if isinstance(v, str):
                setattr(self, k, v)
            else:
                setattr(self, k, v)

    @staticmethod
    def client_json(client):
        # There is better ways to do this, but we don't want to send everything about
        # a client over the tubes.
        return {
            "client_output_muted": client.client_output_muted,
            "client_database_id": client.client_database_id,
            "client_away_message": client.client_away_message,
            "client_country": client.client_country,
            "client_is_priority_speaker": client.client_is_priority_speaker,
            "client_channel_group_id": client.client_channel_group_id,
            "client_outputonly_muted": client.client_outputonly_muted,
            "client_nickname": client.client_nickname,
            "client_description": client.client_description,
            "client_servergroups": client.client_servergroups,
            "client_icon_id": client.client_icon_id,
            "client_input_muted": client.client_input_muted,
            "client_badges": client.client_badges,
            "client_away": client.client_away,
            "cid": client.cid,
            "client_platform": client.client_platform,
            "client_is_channel_commander": client.client_is_channel_commander,
            "client_talk_power": client.client_talk_power,
            "clid": client.clid
        }


    @staticmethod
    def clients_json(clients):
        return [Client.client_json(client) for client in clients]

    def __str__(self):
        return str(Client.client_json(self))

    def __repr__(self):
        return self.__str__()
