import time

from aioxmpp import JID
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import spade.presence
import spade.trace
from MasterAgent import MasterAgent
import sys

class CheckerAgent(Agent):
    jids = [JID]


    class Behav1(OneShotBehaviour):
        def on_available(self, jid, stanza):
            print("[{}] Agent {} is available.".format(self.agent.name, jid.split("@")[0]))
        def on_unavailable(self, jid, stanza):
            print("[{}] Agent {} is unavailable.".format(self.agent.name, jid.split("@")[0]))
        def on_subscribed(self, jid):
            print("[{}] Agent {} has accepted the subscription.".format(self.agent.name, jid.split("@")[0]))
            print("[{}] Contacts List: {}".format(self.agent.name, self.agent.presence.get_contacts()))

        def on_subscribe(self, jid):
            print("[{}] Agent {} asked for subscription. Let's aprove it.".format(self.agent.name, jid.split("@")[0]))
            self.presence.approve(jid)

        async def run(self):
            self.presence.on_subscribe = self.on_subscribe
            self.presence.on_subscribed = self.on_subscribed
            self.presence.on_available = self.on_available
            self.presence.on_unavailable = self.on_unavailable

            self.presence.set_available()
            self.presence.subscribe(self.agent.jids[0])
            self.presence.subscribe(self.agent.jids[1])
            self.presence.subscribe(self.agent.jids[2])

    def getJids(self, jids2):
        contacts = self.presence.get_contacts()
        self.jids = jids2
        print(str(self.jids[0]))
        print(str(contacts[self.jids[0]]))

    async def setup(self):
        print("SEND: CheckerAgent started")
        self.add_behaviour(self.Behav1())
