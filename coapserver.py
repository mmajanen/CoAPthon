#!/usr/bin/env python

import getopt
import sys
from coapthon.server.coap import CoAP
from exampleresources import BasicResource, Long, Separate, Storage, Big, voidResource, XMLResource, ETAGResource, \
    Child, \
    MultipleEncodingResource, AdvancedResource, AdvancedResourceSeparate, \
    HSMLsensorResource, SensorItemResource #MiM

__author__ = 'Giacomo Tanganelli; for HSML support: Mikko Majanen' #MiM


class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self, (host, port), multicast)

        #TODO: remove other resources than HSMLsensorResource (MiM)
        #self.add_resource('basic/', BasicResource())
        #self.add_resource('storage/', Storage())
        #self.add_resource('separate/', Separate())
        #self.add_resource('long/', Long())
        #self.add_resource('big/', Big())
        #self.add_resource('void/', voidResource())
        #self.add_resource('xml/', XMLResource())
        #self.add_resource('encoding/', MultipleEncodingResource())
        #self.add_resource('etag/', ETAGResource())
        #self.add_resource('child/', Child())
        #self.add_resource('advanced/', AdvancedResource())
        #self.add_resource('advancedSeparate/', AdvancedResourceSeparate())

        self.add_resource('sensors/', HSMLsensorResource(coap_server=self)) #MiM

        ctlist=[0, 22001, 22002]
        newRes1 = SensorItemResource(name="temp", coap_server=self)
        newRes1.content_type=ctlist
        newRes1.resource_type="sensor.temp"
        newRes1.interface_type=["hsml.item", "hsml.link"]
        newRes1.payload="23"
        
        print("payload: ", newRes1.payload)
        print("temp: ", newRes1.content_type, newRes1.resource_type, newRes1.interface_type)
        
        newRes2 = SensorItemResource(name="humid", coap_server=self)
        newRes2.content_type=ctlist
        newRes2.resource_type="sensor.humid"
        newRes2.interface_type=["hsml.item", "hsml.link"]
        newRes2.payload="67"
        
        self.add_resource('sensors/temp/', newRes1)
        self.add_resource('sensors/humid/', newRes2)
        """
        {"temp": {"href": "temp", "rel": "item", "n": "temp", "v": 23, "rt": "sensor.temp", "if": "application/hsml.item", "ct": [0, 22001, 22002]},
         {"humid": {"href": "humid", "rel": "item", "n": "humid", "v": 45, "rt": "sensor.humid", "if": "application/hsml.item", "ct": [0, 22001, 22002]}}}
        """        
        print "CoAP Server start on " + host + ":" + str(port)
        print self.root.dump()


def usage():  # pragma: no cover
    print "coapserver.py -i <ip address> -p <port>"


def main(argv):  # pragma: no cover
    ip = "0.0.0.0"
    port = 5683
    multicast = False
    try:
        opts, args = getopt.getopt(argv, "hi:p:m", ["ip=", "port=", "multicast"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-m", "--multicast"):
            multicast = True

    server = CoAPServer(ip, port, multicast)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print "Server Shutdown"
        server.close()
        print "Exiting..."


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
