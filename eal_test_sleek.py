#!/usr/bin/python

# The standard sleek example echo bot, modified to do some androidy
# stuff


import time
import logging

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

import androidhelper
droid = androidhelper.Android()

class EchoBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        # If you wanted more functionality, here's how to register plugins:
        # self.register_plugin('xep_0030') # Service Discovery
        # self.register_plugin('xep_0199') # XMPP Ping

        # Here's how to access plugins once you've registered them:
        # self['xep_0030'].add_feature('echo_demo')

        # If you are working with an OpenFire server, you will
        # need to use a different SSL version:
        # import ssl
        # self.ssl_version = ssl.PROTOCOL_SSLv3

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

        # Most get_*/set_* methods from plugins use Iq stanzas, which
        # can generate IqError and IqTimeout exceptions
        #
        # try:
        #     self.get_roster()
        # except IqError as err:
        #     logging.error('There was an error getting the roster')
        #     logging.error(err.iq['error']['condition'])
        #     self.disconnect()
        # except IqTimeout:
        #     logging.error('Server is taking too long to respond')
        #     self.disconnect()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            if msg['body'] == 'quit':
                self.disconnect()
            elif msg['body'] == 'roster':
                msg.reply("roster: %s" % self.roster).send()
                pass
            elif msg['body'] == 'dir':
                msg.reply(str(dir(self))).send()
            elif msg['body'] == 'bat':
                msg.reply(str(droid.batteryGetLevel())).send()
            elif msg['body'] == 'speak':
                droid.ttsSpeak('test')
            elif msg['body'] == 'contacts':
                msg.reply(str(droid.contactsGetCount())).send()
            elif msg['body'] == 'locate':
                droid.startLocating(1000, 0)
                msg.reply('started Locating')
            elif msg['body'] == 'location':
                msg.reply(str(droid.getLastKnownLocation())).send()
            elif msg['body'] == 'sense':
                droid.startSensingTimed(1, 1000)
                msg.repy('started Sensing').send()
            elif msg['body'] == 'sensors':
                msg.reply(str(droid.readSensors())).send()
            elif msg['body'] == 'droid':
                msg.reply(str(dir(droid))).send()
            elif msg['body'].startswith('call '):
                method = msg['body'].split(' ')[1]
                args = msg['body'].split(' ')[2:]
                result = apply(droid.__getattr__(method), args)
                msg.reply(str(result)).send()
            else: 
                msg.reply("--> %(body)s" % msg).send()


if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    xmpp = EchoBot('someone@some.server', 'password')
    xmpp.connect()
    xmpp.process(block=True)
