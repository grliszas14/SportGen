import time

from aioxmpp import JID, PresenceType
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from aioxmpp import Presence
from spade.message import Message
from spade.template import Template
import spade.presence
import spade.trace
from MasterAgent import MasterAgent
import sys

class CheckerAgent(Agent):
    jids = [JID]
    contacts = None

    class Behav1(OneShotBehaviour):
        def on_available(self, jid, stanza):
            print("[{}] Agent {} is available.".format(self.agent.name, jid.split("@")[0]))
        def on_unavailable(self, jid, stanza):
            jid = jid.split("/")[0]
            print("[{}] Agent {} is unavailable.".format(self.agent.name, jid.split("@")[0]))
            if(jid.split("/")[0] == str(self.agent.jids[0])):
                if(self.agent.contacts[self.agent.jids[1]]["presence"].type_ is PresenceType.AVAILABLE):
                    self.agent.add_behaviour(self.agent.SendBehav2())
                elif (self.agent.contacts[self.agent.jids[2]]["presence"].type_ is PresenceType.AVAILABLE):
                    self.agent.add_behaviour(self.agent.SendBehav3())
                else:
                    raise Exception("nie ma dostępnych agentow!")
                    print("nie ma agentow")

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
            for jid in self.agent.jids:
                self.presence.subscribe(jid)
            self.presence.subscribe(self.agent.jids[1])
            self.presence.subscribe(self.agent.jids[2])

    class SendBehav2(OneShotBehaviour):
        async def run(self):
            msg = Message(to="sportgen2@404.city")  # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "_change_"  # Set the message content
            await self.send(msg)


    class SendBehav3(OneShotBehaviour):
        async def run(self):
            msg = Message(to="sportgen3@404.city")  # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "_change_"  # Set the message content
            await self.send(msg)

    class GetJids(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=15)
            if msg:
                print(msg.sender)
                print(type(msg.sender))
                self.agent.jids.append(msg.sender)
                self.agent.presence.subscribe(msg.sender)
                print("Nowy JID: {}".format(str(msg.sender)))
            else:
                print("no new JIDs")

    def getJids(self, jids2):
        self.jids = jids2
        self.contacts = self.presence.get_contacts()
        print(self.contacts[self.jids[1]]["presence"].type_)
        print(type(self.contacts[self.jids[1]]["presence"].type_))

    async def setup(self):

        print("SEND: CheckerAgent started")
        self.add_behaviour(self.Behav1())
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(self.GetJids(), template)
