import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import spade.presence
import spade.trace
import asyncio

line_no = 0
class InsertAgent(Agent):

    class InformBehav(PeriodicBehaviour):
        async def run(self):
            #pass
            global line_no
            msg = Message(to="sportgen2@404.city")
            msg.set_metadata("performative", "inform")

            with open('../mecz.txt') as fp:
                for i, line in enumerate(fp):
                    if i == (line_no):
                        msg.body = line

            if(msg.body != None):
                await self.send(msg)
                line_no = line_no + 1

    async def setup(self):
        #print("INST: InsertAgent started")
        b = self.InformBehav(period=10)
        self.add_behaviour(b)

