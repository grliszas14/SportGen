import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import spade.presence
import spade.trace

class InsertAgent(Agent):

    class InformBehav(PeriodicBehaviour):
        pass

    async def setup(self):
        print("INST: InsertAgent started")
        b = self.InformBehav(period=5)
        self.add_behaviour(b)
