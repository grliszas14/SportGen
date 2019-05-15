import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template


class SenderAgent(Agent):
    class InformBehav(PeriodicBehaviour):
        async def run(self):
            print("SEND: InformBehav running")
            sendTry = 1
            msg = Message(to="sportgen@404.city")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Hello World"                    # Set the message content

            while (sendTry <= 3):
                await self.send(msg)
                print("SEND: Message sent!")

                response = await self.receive(timeout=10) #TODO: consider changing timeout
                if response:
                    print("SEND: Receiver response: {}".format(response.body))
                    #TODO: consider if (response.body == "OK") maybe?
                    sendTry = 1
                    break
                else:
                    if (sendTry == 3):
                        print("SEND: Receiver is dead, taking its duties.")
                        #TODO: making receiver
                        break
                    sendTry = sendTry + 1
                    print("SEND: Confirmation missing, trying again ({}/3)".format(sendTry))
            # stop agent from behaviour
            # await self.agent.stop()

    async def setup(self):
        print("SEND: SenderAgent started")
        b = self.InformBehav(period=5)
        self.add_behaviour(b)

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
    receiveragent = ReceiverAgent("sportgen@404.city", "dupaelka101")
    future = receiveragent.start()
    future.result() # wait for receiver agent to be prepared.
    receiveragent.web.start(hostname="127.0.0.1", port="10000")
    senderagent = SenderAgent("sportgen2@404.city", "dupaelka101")
    senderagent.start()
    senderagent.web.start(hostname="127.0.0.1", port="10001")

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break
    print("Agents finished")