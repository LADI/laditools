import dbus

name_base = 'org.jackaudio'
controller_interface_name = name_base + '.JackController'
service_name = name_base + '.service'

class jack_controller:
        def __init__(self):
                 self.bus = dbus.SessionBus()
                 self.controller = self.bus.get_object(service_name, "/DefaultController")
                 self.iface = dbus.Interface(self.controller, controller_interface_name)

        def is_started(self):
                return self.iface.IsStarted()

        def is_realtime(self):
                return self.iface.GetEngineParameterValueBool("realtime")

        def get_load(self):
                return self.iface.GetLoad()

        def get_xruns(self):
                return self.iface.GetXruns()

        def get_sample_rate(self):
                return self.iface.GetSampleRate()

        def get_latency(self):
                return self.iface.GetLatency()

        def start(self):
                self.iface.StartServer()

        def stop(self):
                self.iface.StopServer()

        def kill(self):
                self.iface.Exit()
