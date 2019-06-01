import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import spade.presence
import spade.trace

class SenderAgent(Agent):
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

class ReceiverAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("RECV: RecvBehav running")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print("RECV: Message received with content: {}".format(msg.body))
                response = Message(to=str(msg.sender))
                response.set_metadata("performative", "inform")
                response.body = "OK"
                await self.send(response)
            else:
                print("RECV: Did not received any message after 10 seconds")

            # stop agent from behaviour
            # await self.agent.stop()

    async def setup(self):
        print("RECV: ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)



if __name__ == "__main__":
    # order in which ask senders to become receivers in case receiver
    # lost its communication
    senderList = ["sportgen2@404.city", "sportgen3@404.city",
                  "sportgen4@404.city"]

    receiveragent = ReceiverAgent("sportgen@404.city", "dupaelka101")
    future = receiveragent.start()
    future.result() # wait for receiver agent to be prepared.
    receiveragent.web.start(hostname="127.0.0.1", port="10000")

    senderagent2 = SenderAgent("sportgen2@404.city", "dupaelka101")
    senderagent2.start()
    senderagent2.web.start(hostname="127.0.0.1", port="10001")

    senderagent3 = SenderAgent("sportgen3@404.city", "dupaelka101")
    senderagent3.start()
    senderagent3.web.start(hostname="127.0.0.1", port="10002")

    senderagent4 = SenderAgent("sportgen4@404.city", "dupaelka101")
    senderagent4.start()
    senderagent4.web.start(hostname="127.0.0.1", port="10003")

    i = 1

    while receiveragent.is_alive():
        try:
            time.sleep(1)
            # recv dead simulation
            #if i < 10:
            #    time.sleep(1)
            #    i = i + 1
            #elif i == 10:
            #    print('Killing receiver')
            #    receiveragent.stop()
            #    print('Receiver killed')
            #    i = i + 1
            #else:
            #    time.sleep(1)
        except KeyboardInterrupt:
            senderagent2.stop()
            senderagent3.stop()
            senderagent4.stop()
            receiveragent.stop()
            break
    print("Agents finished")