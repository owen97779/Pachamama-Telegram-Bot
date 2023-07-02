import asyncio
from ping3 import ping
from utils import notify


class Host(object):
    '''
    Host class to ping only instantiated host objects and keep track of flags.
    '''
    def __init__(self, host_name: str, ip: str):
        '''
        Function to instantiate the Host class as an object which can be pinged.
        
        Parameters
        ----------
        host_name: str
            Name of the host.
        ip: str
            Pingable FQDN/IP.
        '''
        self.host_name = host_name
        self.ip = ip
        self.pinginfo = {
            "average_ping": 0,
            "ping_count": 0,
            "status": False,
            "success_rate": 0,
            "ping_times": [],
        }
        self.down_notify_flag = False
        self.old_down_notify_flag = False
        self.amber_notify_flag = False
        self.old_amber_notify_flag = False
        self.red_notify_flag = False
        self.old_red_notify_flag = False

    def ping(self, max_count: int, unit="ms"):
        '''
        Function to fill the pinginfo dictionary with ping information using averages.

        Parameters
        ----------
        max_count: int
            Number of times to ping the host.
        unit: str
            Unit of time to measure ping in.
        '''
        ping_total = 0
        ping_count = 0
        ping_time = []
        for i in range(max_count):
            ping_ = ping(dest_addr=self.ip, unit=unit, timeout=1)
            if ping_ == None:
                print(f"{self.host_name} - Ping failed")
            else:
                ping_total += ping_
                ping_count += 1
                ping_time.append(round(ping_,2))
        if ping_count == 0:
            self.pinginfo["average_ping"] = 0
            self.pinginfo["ping_count"] = 0
            self.pinginfo["status"] = False
            self.pinginfo["success_rate"] = 0
            self.pinginfo["ping_times"] = ["N/A"]
        else:
            average_ping = ping_total / ping_count
            self.pinginfo["average_ping"] = round(average_ping, 2)
            self.pinginfo["ping_count"] = ping_count
            self.pinginfo["status"] = True
            self.pinginfo["success_rate"] = ping_count / max_count
            self.pinginfo["ping_times"] = ping_time

    def reset_flags(self):
        '''
        Function to reset all flags to False.
        '''
        self.old_down_notify_flag = self.down_notify_flag
        self.old_amber_notify_flag = self.amber_notify_flag
        self.old_red_notify_flag = self.red_notify_flag

        self.down_notify_flag = False
        self.amber_notify_flag = False
        self.red_notify_flag = False

    def check_flag_change(self):
        '''
        Function to check if any flags have changed.
        Returns
        -------
        bool
            True if any flags have changed, False if not.
        '''
        if (
            self.old_down_notify_flag != self.down_notify_flag
            or self.old_amber_notify_flag != self.amber_notify_flag
            or self.old_red_notify_flag != self.red_notify_flag
        ):
            return True
        else:
            return False

    def green(self):
        '''
        Function to reset all flags and check if any flags have changed.
        Returns
        -------
        int
            0 if no flags have changed, -1 if flags have changed.
        '''
        self.reset_flags()
        if self.check_flag_change():
            return 0
        else:
            return -1

    def amber(self):
        '''
        Function to set amber flag and check if any flags have changed.
        Returns
        -------
        int
            1 if amber flag has changed, -1 if flags have changed.
        '''
        self.reset_flags()
        self.amber_notify_flag = True
        if self.check_flag_change():
            return 1
        else:
            return -1

    def red(self):
        '''
        Function to set red flag and check if any flags have changed.
        Returns
        -------
        int
            2 if red flag has changed, -1 if flags have changed.
        '''
        self.reset_flags()
        self.red_notify_flag = True
        if self.check_flag_change():
            return 2
        else:
            return -1

    def down(self):
        '''
        Function to set down flag and check if any flags have changed.
        Returns
        -------
        int
            3 if down flag has changed, -1 if flags have changed.
        '''
        self.reset_flags()
        self.down_notify_flag = True
        if self.check_flag_change():
            return 3
        else:
            return -1
