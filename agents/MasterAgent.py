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
			#print("RECV: RecvBehav running")
            msg = await self.receive(timeout=15) # wait for a message for 10 seconds
            if msg:
                print("{}".format(msg.body))
                #response = Message(to=str(msg.sender))
                #response.set_metadata("performative", "inform")
                #response.body = "OK"
                #await self.send(response)
            else:
                print("RECV: Did not received any message after 10 seconds")

            # stop agent from behaviour
            # await self.agent.stop()

    async def setup(self):
        #print("RECV: ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
