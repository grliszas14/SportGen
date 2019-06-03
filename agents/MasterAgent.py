import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import spade.presence
import spade.trace

class MasterAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=15) # wait for a message for 10 seconds
            if msg:
                print("{}".format(msg.body))
                response = Message(to=str(msg.sender))
                response.set_metadata("performative", "inform")
                response.body = "OK"
                #await self.send(response)
            else:
                print("MAST: Did not received any message after 10 seconds")

    class HelloChecker(OneShotBehaviour):
        async def run(self):
            msg = Message(to="sportgenChecker@404.city")  # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "hello"  # Set the message content
            await self.send(msg)



    async def setup(self):
        print("MAST: MasterAgent started")
        self.add_behaviour(self.HelloChecker())
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
