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

            return parsed


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


    # Revive.Config Class
    class Config(Connect):
        """
        Revive API configuration class

            Creates subclasses:
                revive.config.network
                revive.config.watchdog
        """

        def __init__(self):
            self.settings = self.settings()     # All settings from Revive
            self.network  = self.Network(self)  # revive.config.network class
            self.watchdog = self.Watchdog(self) # revive.config.watchdog class

        def settings(self):
            # GET /v1/api/config/get
            request  = self.request("GET", "/v1/api/config/get")
            settings = json.loads(request)

            # Everything we care about is under data: { }
            return settings["data"]


        # Revive.Config.Network Class
        class Network:
            """
            Revive API network configuration:

                Sets variables:
                    revive.config.network.settings     [dictionary]

                    revive.config.network.mode         [string/rw]
                    revive.config.network.ip           [string/rw]
                    revive.config.network.netmask      [string/rw]
                    revive.config.network.gateway      [string/rw]
                    revive.config.network.primaryDNS   [string/rw]
                    revive.config.network.secondaryDNS [string/rw]
            """

            # Initialize with the network settings pulled from parent class
            def __init__(self, parent):
                self.parent       = parent
                self.settings     = self.parent.settings["network"]

                self.mode         = self.settings["mode"]
                self.ip           = self.settings["ip"]
                self.netmask      = self.settings["netmask"]
                self.gateway      = self.settings["gateway"]
                self.primaryDNS   = self.settings["primaryDNS"]
                self.secondaryDNS = self.settings["secondaryDNS"]

            # Writes all settings back to the Revive via a PATCH request
            # revive.config.network.save()
            def save(self):
                """Write all of the network settings back to the device"""

                # Accept either: dhcp or manual
                if self.mode.lower() not in [ "dhcp", "manual" ]:
                    raise Exception("Invalid mode.  Valid modes: dhcp, manual")

                # Simple JSON if we are doing DHCP
                if self.mode.lower() == "dhcp":
                    settings = json.dumps({ "network": { "mode": "dhcp" } })

                # Build out the dict with the settings
                else:
                    settings = {
                        "network": {
                            "mode": "manual",
                            "ip": self.ip,
                            "netmask": self.netmask,
                            "gateway": self.gateway,
                            "primaryDNS": self.primaryDNS,
                            "secondaryDNS": self.secondaryDNS
                        }
                    }

                    # Then convert it to JSON for the PATCH request to the API
                    settings = json.dumps(settings)

                # PATCH to /v1/api/config/update with JSON settings payload
                request = self.parent.request("PATCH", "/v1/api/config/update", settings)

                return request



            # Print out the Revive network settings all pretty like
            def show(self):
                """Show the Revive network settings"""
                print "Mode:          " + self.mode
                print "IP address:    " + self.ip
                print "Netmask:       " + self.netmask
                print "Gateway:       " + self.gateway
                print "Primary DNS:   " + self.primarydns
                print "Secondary DNS: " + self.secondarydns


        class Watchdog:
            """
            Revive API watchdog configuration:

                Sets variables:
                    revive.config.watchdog.settings          [dictionary]

                    revive.config.watchdog.pingInterval      [integer/rw]
                    revive.config.watchdog.firstResetAfter   [integer/rw]
                    revive.config.watchdog.anotherResetEvery [integer/rw]
            """

            # Initialize with the watchdog settings pulled from parent class
            def __init__(self, parent):
                self.parent            = parent
                self.settings          = self.parent.settings["watchdog"]

                self.pingInterval      = self.settings["pingInterval"]
                self.firstResetAfter   = self.settings["firstResetAfter"]
                self.anotherResetEvery = self.settings["anotherResetEvery"]

            # Writes all settings back to the Revive via a PATCH request
            # revive.config.watchdog.save()
            def save(self):
                """Write all of the watchdog settings back to the device"""

                test = { "pingInterval": self.pingInterval, "firstResetAfter": self.firstResetAfter, "anotherResetEvery": self.anotherResetEvery }

                # Test and make sure that all settings are integers
                for key, val in test.iteritems():
                    if not isinstance(val, int):
                        error = "%s value '%s' is not an integer." % (key, val)
                        raise Exception(error)

                # Create a dictionary with the watchdog settings
                settings = {
                    "watchdog": {
                        "pingInterval": int(self.pingInterval),
                        "firstResetAfter": int(self.firstResetAfter),
                        "anotherResetEvery": int(self.anotherResetEvery)
                    }
                }

                # Then convert it to JSON for the PATCH request to the API
                settings = json.dumps(settings)

                # PATCH to /v1/api/config/update with JSON settings payload
                request = self.parent.request("PATCH", "/v1/api/config/update", settings)

                return request



            # Print out the Revive network settings all pretty like
            def show(self):
                """Show the Revive watchdog settings"""
                print "Ping Interval:       %d" % self.pingInterval
                print "First Reset After:   %d" % self.firstResetAfter
                print "Another Reset Every: %d" % self.anotherResetEvery


# EOF
