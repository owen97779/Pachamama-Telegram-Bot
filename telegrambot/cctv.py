import aiomqtt
import datetime
from utils import notify

class CCTVmember(object):
    """
    CCTVmember class which stores the name of the member, the time they logged in and out, and whether they are logged in or out.
    """

    def __init__(self, name):
        """
        Initialises the CCTVmember class with the name of the member, and sets the logged in and logged out times to empty strings.

        Parameters
        ----------
        name : str
            The name of the member.
        """
        self.name = name
        self.logged_in = False
        self.logged_in_time = ""
        self.logged_out = True
        self.logged_out_time = ""

    def get_time(self):
        """
        Gets the current time and returns it in the format HH:MM:SS.

        Returns
        -------
        formatted_time: str
            The current time in the format HH:MM:SS.
        """
        time = datetime.datetime.now()
        hour = time.hour
        minute = time.minute
        second = time.second
        if hour < 10:
            hour = f"0{hour}"
        if minute < 10:
            minute = f"0{minute}"
        if second < 10:
            second = f"0{second}"
        formatted_time = f"{hour}:{minute}:{second}"
        return formatted_time

    def login(self):
        """
        Keeps track of the time the member logged in, and sets the logged in and logged out variables to True and False respectively.
        """
        self.logged_in = True
        self.logged_in_time = self.get_time()
        self.logged_out = False

    def logout(self):
        """
        Keeps track of the time the member logged out, and sets the logged in and logged out variables to False and True respectively.
        """
        self.logged_out = True
        self.logged_out_time = self.get_time()
        self.logged_in = False


class CCTV(object):
    """
    Class which stores the CCTV members and their login and logout times. It also handles the MQTT connection and subscribes to the BlueIris/# topic.
    """

    def __init__(self, server, sub):
        """
        Initialises the CCTV class with the MQTT server and the topic to subscribe to.

        Parameters
        ----------
        server : str
            The MQTT server to connect to.
        sub : str
            The topic to subscribe to.
        """
        self.members = {}
        self.server = server
        self.sub = sub

    async def connect(self, store, TOKEN):
        """
        Establishes a connection to the MQTT server and subscribes to the topic. It then listens for messages and parses them to get the name of the member and whether they logged in or out.

        Parameters
        ----------
        subscribers : list
            A list of subscribers to notify when a member logs in or out.
        TOKEN : str
            The Telegram bot token.
        """
        async with aiomqtt.Client(self.server) as client:
            async with client.messages() as messages:
                await client.subscribe(self.sub)
                async for message in messages:
                    print(message.payload)
                    words = str.split(message.payload.decode())
                    name = words[0].lower()
                    log = words[2].lower()

                    if name not in self.members:
                        self.members[name] = CCTVmember(name)

                    if log == "in":
                        self.members[name].login()
                        print(self.members)
                        print(
                            f"{self.members[name].name} logged in at {self.members[name].logged_in_time}"
                        )

                    elif log == "out":
                        self.members[name].logout()
                        date = datetime.datetime.now()
                        formatted_date = date.strftime("%d/%m/%y")
                        msg = f"""
                        📸 {self.members[name].name.capitalize()} CCTV Login Time: 
                        \n[{formatted_date}]        {self.members[name].logged_in_time} - {self.members[name].logged_out_time}
                        """
                        print(msg)
                        cctv_chatids = [
                            key
                            for key, value in store.subscribers.items()
                            if "cctv_sub" in value and value["cctv_sub"]
                        ]

                        await notify(msg, cctv_chatids, TOKEN)
