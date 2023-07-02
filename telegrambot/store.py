import json
from ping import Host


class Store(object):
    """
    Store class which stores the hosts and subscribers from JSON files to be used by the bot.
    """
    def __init__(self, hosts_file: str, subs_file: str):
        """
        Initialises the Store class with the hosts and subscribers.

        Parameters
        ----------
        hosts_file: str
            The name of the JSON file containing the hosts.
        subs_file: str
            The name of the JSON file containing the subscribers.
        """
        self.hosts_file = hosts_file
        self.subs_file = subs_file
        self.hostobj = {}
        self.allhosts = {}
        self.subscribers = []

    def load(self):
        """
        Loads the hosts and subscribers from the JSON files into the Store class.

        Parameters
        ----------
        hosts_file: str
            The name of the JSON file containing the hosts.
        subs_file: str
            The name of the JSON file containing the subscribers.
        """
        with open("subscribers.json", "r") as file:
            data = json.load(file)
            self.subscribers = data["subscribers"]

        with open("hosts.json", "r") as hosts_file:
            self.allhosts = json.load(hosts_file)
        for host in self.allhosts:
            self.hostobj[host] = Host(host, self.allhosts[host])

    def add_host(self, host: str, ip: str):
        """
        Adds the hostobjs to the JSON file and the hostobj dictionary.

        Parameters
        ----------
        host: str
            The name of the host to be added.
        ip: str
            The IP of the host to be added.
        """
        self.allhosts[host] = ip
        with open(self.hosts_file, "w") as hosts_file:
            json.dump(self.allhosts, hosts_file)
        self.hostobj[host] = Host(host, ip)

    def remove_host(self, host: str):
        """
        Removes the hostobjs from the JSON file and the hostobj dictionary.

        Parameters
        ----------
        host: str
            The name of the host to be removed.
        """
        del self.allhosts[host]
        with open(self.hosts_file, "w") as hosts_file:
            json.dump(self.allhosts, hosts_file)
        del self.hostobj[host]

    def add_subscriber(self, chatid: int):
        """
        Adds the subscriber to the JSON file and the subscribers list.

        Parameters
        ----------
        chatid: int
            The chatid of the subscriber to be added.
        """
        self.subscribers.append(chatid)
        with open(self.subs_file, "w") as file:
            json.dump({"subscribers": self.subscribers}, file)

    def remove_subscriber(self, chatid: int):
        """
        Removes the subscriber from the JSON file and the subscribers list.

        Parameters
        ----------
        chatid: int
            The chatid of the subscriber to be removed.
        """
        self.subscribers.remove(chatid)
        with open(self.subs_file, "w") as file:
            json.dump({"subscribers": self.subscribers}, file)
