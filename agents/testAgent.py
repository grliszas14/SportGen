import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import spade.presence
import spade.trace
from MasterAgent import MasterAgent
from TemplateAgent import TemplateAgent
from InsertAgent import InsertAgent
from CheckerAgent import CheckerAgent

if __name__ == "__main__":
    # order in which ask senders to become receivers in case receiver
    # lost its communication
    senderList = ["sportgen2@404.city", "sportgen3@404.city",
                  "sportgen4@404.city"]

    checkerAgent = CheckerAgent("sportgenchecker@404.city", "dupaelka101")
    futureChecker = checkerAgent.start()
    futureChecker.result()
    checkerAgent.web.start(hostname="127.0.0.1", port="10005")

    masterAgent = MasterAgent("sportgen@404.city", "dupaelka101")
    future = masterAgent.start()
    future.result() # wait for receiver agent to be prepared.
    masterAgent.web.start(hostname="127.0.0.1", port="10000")

    templateAgent = TemplateAgent("sportgen2@404.city", "dupaelka101")
    future2 = templateAgent.start()
    future2.result()
    templateAgent.web.start(hostname="127.0.0.1", port="10001")

    insertAgent = InsertAgent("sportgen3@404.city", "dupaelka101")
    future3 = insertAgent.start()
    future3.result()
    insertAgent.web.start(hostname="127.0.0.1", port="10002")


    #senderagent4 = SenderAgent("sportgen4@404.city", "dupaelka101")
    #senderagent4.start()
    #senderagent4.web.start(hostname="127.0.0.1", port="10003")

    i = 1


