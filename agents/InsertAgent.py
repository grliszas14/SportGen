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

    class HelloChecker(OneShotBehaviour):
        async def run(self):
            msg = Message(to="sportgenChecker@404.city")  # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "hello"  # Set the message content
            await self.send(msg)



    async def setup(self):
        print("INST: InsertAgent started")
        self.add_behaviour(self.HelloChecker())
        b = self.InformBehav(period=10)
        self.add_behaviour(b)

