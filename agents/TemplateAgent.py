import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import spade.presence
import spade.trace
from MasterAgent import MasterAgent
import sys
sys.path.insert(0, '../models')
from data2language import Data2Language

class TemplateAgent(Agent):
    class MakeSentenceBehav(OneShotBehaviour):
        async def run(self):
            print('SIEMA')

    class InformBehav(PeriodicBehaviour):
        async def run(self):
            d2l = Data2Language()
            message = ''
            response = await self.receive(timeout=60)
            print("SEND: Got message from inserter")
            # parse message
            team, player, minute, action, action_type = response.body.split(',')
            print(team)
            print(player)
            print(minute)
            print(action)
            print(action_type)
            try:
                message = d2l.apply_template(team, player, minute, action, action_type)
                print(message)
            except:
                print('Cannot make sentence')
            msg = Message(to="sportgen@404.city")       # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = str(message)                              # Set the message content

            await self.send(msg)


    async def setup(self):
        print("SEND: SenderAgent started")
        b = self.InformBehav(period=5)
        self.add_behaviour(b)
        #TODO: making receiver
        #c = self.MakeSentenceBehav()
        #templateS = Template()
        #templateS.thread = "None"
        #templateS.metadata={}
        #templateS.sender="sportgen3@404.city"
        #self.add_behaviour(c, templateS)
