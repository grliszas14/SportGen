import time

from agents.InsertAgent import InsertAgent
from agents.TemplateAgent import TemplateAgent
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
    jids = []
    contacts = None
    replacer = 0

    class Behav1(OneShotBehaviour):
        def on_available(self, jid, stanza):
            print("[{}] Agent {} is available.".format(self.agent.name, jid.split("@")[0]))
            if(jid.split("/")[0] == "sportgen@404.city" and self.agent.replacer != 0):
                self.agent.add_behaviour(self.agent.MasterBehav())
        def on_unavailable(self, jid, stanza):
            jid = jid.split("/")[0]
            print("[{}] Agent {} is unavailable.".format(self.agent.name, jid.split("@")[0]))
            if(jid.split("/")[0] == "sportgen@404.city"):
                if self.agent.jids[1] != None:
                    if(self.agent.contacts[self.agent.jids[2]]["presence"].type_ is PresenceType.AVAILABLE):
                        self.agent.add_behaviour(self.agent.SendBehav2())
                        self.replacer = 1
                    elif (self.agent.contacts[self.agent.jids[1]]["presence"].type_ is PresenceType.AVAILABLE):
                        self.agent.add_behaviour(self.agent.SendBehav3())
                        self.replacer = 2
                    else:
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


    class SendBehav2(OneShotBehaviour):
        async def run(self):
            self.agent.replacer = 1
            masterAgent = MasterAgent("sportgen3@404.city", "dupaelka101")
            await masterAgent.start()
            masterAgent.web.start(hostname="127.0.0.1", port="10000")

    class SendBehav3(OneShotBehaviour):
        async def run(self):
            self.agent.replacer = 2
            masterAgent = MasterAgent("sportgen2@404.city", "dupaelka101")
            await masterAgent.start()
            masterAgent.web.start(hostname="127.0.0.1", port="10000")

    class MasterBehav(OneShotBehaviour):
        async def run(self):
            if self.agent.replacer == 1:
                insertAgent = InsertAgent("sportgen3@404.city", "dupaelka101")
                await insertAgent.start()
                insertAgent.web.start(hostname="127.0.0.1", port="10002")
            elif self.agent.replacer == 2:
                templateAgent = TemplateAgent("sportgen3@404.city", "dupaelka101")
                await templateAgent.start()
                templateAgent.web.start(hostname="127.0.0.1", port="10001")
            else:
                print("kto zastapil?")
            masterAgent = MasterAgent("sportgen@404.city", "dupaelka101")
            await masterAgent.start()
            masterAgent.web.start(hostname="127.0.0.1", port="10000")
            self.agent.replacer = 0

    class GetJids(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=15)
            if msg:
                if msg.sender not in self.agent.jids:
                    self.agent.jids.append(msg.sender)
                    print("Nowy JID: {}".format(str(msg.sender)))
                    print(self.agent.jids)
            else:
                print("no new JIDs")

    async def setup(self):
        print("CHECK: CheckerAgent started")
        self.contacts = self.presence.get_contacts()
        self.add_behaviour(self.Behav1())
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(self.GetJids(), template)
