import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import spade.presence
import spade.trace
from MasterAgent import MasterAgent

class TemplateAgent(Agent):
    class MakeSentenceBehav(OneShotBehaviour):
        async def run(self):
            print('SIEMA')

    class InformBehav(PeriodicBehaviour):
        async def run(self):
            print("SEND: InformBehav running")
            sendTry = 1
            msg = Message(to="sportgen@404.city")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Hello World"                    # Set the message content
            #contacts = self.presence.get_contacts() #- check other agents
            #print(contacts)

            while (sendTry <= 3):
                await self.send(msg)
                print(msg.body)
                print("SEND: Message sent!")

                response = await self.receive(timeout=5) #TODO: consider changing timeout
                if response:
                    print("SEND: Receiver response: {}".format(response.body))
                    #TODO: consider if (response.body == "OK") maybe?
                    sendTry = 1
                    break
                else:
                    if (sendTry == 3):
                        if (str(msg.sender) == str(senderList[0])):
                            self.kill()
                            self = ReceiverAgent(senderList[0], "dupaelka101")
                            await self.start()
                            self.web.start(hostname="127.0.0.1", port="10001")
                            print("SEND: Receiver is dead, sender1 is becoming receiver")
                        msg = Message(to="sportgen2@404.city")
                        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                        msg.body = "Hello World2"                    # Set the message content
                        sendTry = 1
                        if (str(msg.sender) == str(senderList[1])):
                            self.kill()
                            self = ReceiverAgent(senderList[1], "dupaelka101")
                            print("SEND: Receiver is dead, sender2 is becoming receiver")
                        msg = Message(to="sportgen3@404.city")
                        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                        msg.body = "Hello World"                    # Set the message content
                        sendTry = 1
                        break
                    sendTry = sendTry + 1
                    print("SEND: Confirmation missing, trying again ({}/3)".format(sendTry))
            # stop agent from behaviour
            # await self.agent.stop()
            #contacts = self.presence.get_contacts() #- check other agents
            #print(contacts)

    async def setup(self):
        print("SEND: SenderAgent started")
        b = self.InformBehav(period=5)
        self.add_behaviour(b)
        #TODO: making receiver
        c = self.MakeSentenceBehav()
        templateS = Template()
        templateS.thread = "None"
        templateS.metadata={}
        self.add_behaviour(c, templateS)
