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
        self.allhosts = {}
        self.hostobj = {}
        self.subscribers = {}

    def load(self):
        """
        Loads the hosts and subscribers from the JSON files into the Store class.
        """
        with open(self.subs_file, "r") as sub_file:
            jsonSubs = json.load(sub_file)
        for key, value in jsonSubs.items():
            self.subscribers[key] = value

        with open(self.hosts_file, "r") as hosts_file:
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

    def add_subscriber(
        self,
        chatid: int,
        sub_dict={
            "cctv_sub": False,
            "status_sub": False,
            "down_sub": False,
            "broadcast_sub": True,
        },
    ):
        """
        Adds the subscriber to the JSON file and the subscribers list.

        Parameters
        ----------
        chatid: int
            The chatid of the subscriber to be added.
        sub_dict: dict
            The dictionary containing the subscription information.
        """
        # Broadcast is true by default
        self.subscribers[chatid] = sub_dict
        with open(self.subs_file, "w") as subs_file:
            json.dump(self.subscribers, subs_file)

    def remove_subscriber(self, chatid: int):
        """
        Removes the subscriber from the JSON file and the subscribers list.

        Parameters
        ----------
        chatid: int
            The chatid of the subscriber to be removed.
        """
        del self.subscribers[chatid]
        with open(self.subs_file, "w") as subs_file:
            json.dump(self.subscribers, subs_file)

    def update_subscriptions(self, sub_type, chatid: int, arguments: str):
        """
        Updates the subscriber's subscriptions.

        Parameters
        ----------
        sub_type: bool
            The subscription type to be updated.
        chatid: int
            The chatid of the subscriber to be updated.
        arguments: str
            The arguments to be updated.
        """
        new_dict = self.subscribers.get(chatid)
        if new_dict == None:
            print("Error subscriber not found, fix code")
        if "cctv" in arguments:
            new_dict["cctv_sub"] = sub_type
        if "status" in arguments:
            new_dict["status_sub"] = sub_type
        if "down" in arguments:
            new_dict["down_sub"] = sub_type
        if "broadcast" in arguments:
            new_dict["broadcast_sub"] = sub_type

        self.subscribers[chatid] = new_dict

        with open(self.subs_file, "w") as subs_file:
            json.dump(self.subscribers, subs_file)
