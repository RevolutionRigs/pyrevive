import json
import requests

METHODS = [ "GET", "POST", "PATCH" ]

def connect(host, key):
    """Initializes Revive API object"""
    return Revive(host, key)

class Revive:
    """
    """


    def __init__(self, host, key):
        global url
        global headers

        self.host = host
        self.key  = key
        self.url  = "http://" + host
        self.headers = { "Authorization": "Bearer " + self.key, "Content-Type": "application/json" }

        url = "http://" + host
        headers = { "Authorization": "Bearer " + self.key, "Content-Type": "application/json" }

        self.rig    = self.Rig()
        self.power  = self.Power()
        self.config = self.Config()
        self.device = self.Device()


    class Connect:
        """Revive Connect class for use in subclasses"""

        @staticmethod
        def request(method, uri, payload=""):

            # GET, POST, PATCH
            if method not in METHODS:
                raise Exception("Unsupported HTTP method: " + method)

            print("%s -> %s -> %s -> %s") % (method, url + uri, payload, headers)

            try:
                response = requests.request(method, url + uri, data=payload, headers=headers)
                parsed   = json.dumps(json.loads(response.text), indent=2, sort_keys=True)
            except:
                raise Exception

            print parsed


    class Power:
        """
        """

        # foo = "{ "login": %s }" % ( "true" )

        def __init__(self):
            """
            """
            #self.port = port
            #self.rig  = port

        def reset(self, port):
            """Restart rig"""
            print("Restarting rig: %2s") % port

        def restart(self, port):
            """Restart rig"""
            self.reset(port)

        def cycle(self, port):
            """Restart rig"""
            self.reset(port)

        def on(self, port):
            """Power rig ON"""
            print("Powering on rig: %2s") % port

        def off(self, port):
            """Power rig OFF"""
            print("Powering off rig: %2s") % port


    class Device(Connect):
        """
        """

        def __init__(self):
            """
            """

        def auth(self):
            """Check Revive Device key"""
            payload = '{ "login": true }'
            return self.request("POST", "/v1/api/device/auth", payload)

        def id(self):
            """Get Revive Device ID"""
            return self.request("GET", "/v1/api/device/id")

        def hello(self):
            """Get Revive Welcome Message"""
            return self.request("GET", "/v1/api/device/hello")


    class Rig(Connect):
        """
        """

        def __init__(self):
            """
            """

        def update(self, port):
            """
            """
            print("Updating rig: %2s") % port

        def get(self):
            """
            """
            print("Getting info for rig: %2s") % port

        def info(self):
            """
            """
            self.get()


    class Config(Connect):
        """
        """

        def __init__(self):
            """
            """
            self.device   = self.Device()
            self.network  = self.Network()
            self.watchdog = self.Watchdog()
            self.settings = self.get()

        def get(self):
            print("Getting Config JSON")
            # GET /v1/api/config/get
            # settings = json.loads(request.text)
            # return settings


        class Device:
            """
            """

            def __init__(self):
                """
                """
                # This way probably --=v
                # self.settings = super(Config, self).settings["device"]

                # self.configurationDone  = super(Config, self).settings["device"]["configurationDone"]

            def save(self):
                """Write all device settings back to the device"""

            def show(self):
                print "configurationDone: " + self.configurationdone


        class Network:
            """
            """

            def __init__(self):
                # This way probably --=v

                # self.ip = super(Config, self).settings["network"]["ip"]

                # self.ip = super(Config, self).get("ip")
                # self.netmask = super(Config, self).get("netmask")
                # self.gateway = super(Config, self).get("gateway")
                # self.primarydns = super(Config, self).get("primarydns")
                # self.secondarydns = super(Config, self).get("secondarydns")

                # settings = super(Config, self).get("network")
                self.ip = "192.168.1.254"
                self.netmask = "255.255.255.0"
                self.gateway = "192.168.1.1"
                self.primarydns = "8.8.8.8"
                self.secondarydns = "8.8.4.4"

            def save(self):
                """Write all of the network settings back to the device"""

            def show(self):
                print "IP address:    " + self.ip
                print "Netmask:       " + self.netmask
                print "Gateway:       " + self.gateway
                print "Primary DNS:   " + self.primarydns
                print "Secondary DNS: " + self.secondarydns


        class Watchdog:
            """
            """

            def __init__(self):
                """
                """


            def save(self):
                """Write all watchdog settings back to the device"""


# EOF
