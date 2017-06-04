import time
from coapthon import defines
from coapthon.resources.resource import Resource

import json

__author__ = 'Giacomo Tanganelli; for HSML support: Mikko Majanen' #MiM

    
class BasicResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(BasicResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "Basic Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    def render_POST(self, request):
        res = self.init_resource(request, BasicResource())
        return res

    def render_DELETE(self, request):
        return True


class Storage(Resource):
    def __init__(self, name="StorageResource", coap_server=None):
        super(Storage, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "Storage Resource for PUT, POST and DELETE"

    def render_GET(self, request):
        return self

    def render_POST(self, request):
        res = self.init_resource(request, BasicResource())
        return res


class Child(Resource):
    def __init__(self, name="ChildResource", coap_server=None):
        super(Child, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = ""

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.payload = request.payload
        return self

    def render_POST(self, request):
        res = BasicResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res

    def render_DELETE(self, request):
        return True


class Separate(Resource):

    def __init__(self, name="Separate", coap_server=None):
        super(Separate, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "Separate"
        self.max_age = 60

    def render_GET(self, request):
        return self, self.render_GET_separate

    def render_GET_separate(self, request):
        time.sleep(5)
        return self

    def render_POST(self, request):
        return self, self.render_POST_separate

    def render_POST_separate(self, request):
        self.payload = request.payload
        return self

    def render_PUT(self, request):
        return self, self.render_PUT_separate

    def render_PUT_separate(self, request):
        self.payload = request.payload
        return self

    def render_DELETE(self, request):
        return self, self.render_DELETE_separate

    def render_DELETE_separate(self, request):
        return True


class Long(Resource):

    def __init__(self, name="Long", coap_server=None):
        super(Long, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "Long Time"

    def render_GET(self, request):
        time.sleep(10)
        return self


class Big(Resource):

    def __init__(self, name="Big", coap_server=None):
        super(Big, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras sollicitudin fermentum ornare. " \
                       "Cras accumsan tellus quis dui lacinia eleifend. Proin ultrices rutrum orci vitae luctus. " \
                       "Nullam malesuada pretium elit, at aliquam odio vehicula in. Etiam nec maximus elit. " \
                       "Etiam at erat ac ex ornare feugiat. Curabitur sed malesuada orci, id aliquet nunc. Phasellus " \
                       "nec leo luctus, blandit lorem sit amet, interdum metus. Duis efficitur volutpat magna, ac " \
                       "ultricies nibh aliquet sit amet. Etiam tempor egestas augue in hendrerit. Nunc eget augue " \
                       "ultricies, dignissim lacus et, vulputate dolor. Nulla eros odio, fringilla vel massa ut, " \
                       "facilisis cursus quam. Fusce faucibus lobortis congue. Fusce consectetur porta neque, id " \
                       "sollicitudin velit maximus eu. Sed pharetra leo quam, vel finibus turpis cursus ac. " \
                       "Aenean ac nisi massa. Cras commodo arcu nec ante tristique ullamcorper. Quisque eu hendrerit" \
                       " urna. Cras fringilla eros ut nunc maximus, non porta nisl mollis. Aliquam in rutrum massa." \
                       " Praesent tristique turpis dui, at ultricies lorem fermentum at. Vivamus sit amet ornare neque, " \
                       "a imperdiet nisl. Quisque a iaculis libero, id tempus lacus. Aenean convallis est non justo " \
                       "consectetur, a hendrerit enim consequat. In accumsan ante a egestas luctus. Etiam quis neque " \
                       "nec eros vestibulum faucibus. Nunc viverra ipsum lectus, vel scelerisque dui dictum a. Ut orci " \
                       "enim, ultrices a ultrices nec, pharetra in quam. Donec accumsan sit amet eros eget fermentum." \
                       "Vivamus ut odio ac odio malesuada accumsan. Aenean vehicula diam at tempus ornare. Phasellus " \
                       "dictum mauris a mi consequat, vitae mattis nulla fringilla. Ut laoreet tellus in nisl efficitur," \
                       " a luctus justo tempus. Fusce finibus libero eget velit finibus iaculis. Morbi rhoncus purus " \
                       "vel vestibulum ullamcorper. Sed ac metus in urna fermentum feugiat. Nulla nunc diam, sodales " \
                       "aliquam mi id, varius porta nisl. Praesent vel nibh ac turpis rutrum laoreet at non odio. " \
                       "Phasellus ut posuere mi. Suspendisse malesuada velit nec mauris convallis porta. Vivamus " \
                       "sed ultrices sapien, at cras amet."

    def render_GET(self, request):
        return self

    def render_POST(self, request):
        if request.payload is not None:
            self.payload = request.payload
        return self


class voidResource(Resource):
    def __init__(self, name="Void"):
        super(voidResource, self).__init__(name)


class XMLResource(Resource):
    def __init__(self, name="XML"):
        super(XMLResource, self).__init__(name)
        self.value = 0
        self.payload = (defines.Content_types["application/xml"], "<value>"+str(self.value)+"</value>")

    def render_GET(self, request):
        return self


class MultipleEncodingResource(Resource):
    def __init__(self, name="MultipleEncoding"):
        super(MultipleEncodingResource, self).__init__(name)
        self.value = 0
        self.payload = str(self.value)
        self.content_type = [defines.Content_types["application/xml"], defines.Content_types["application/json"]]

    def render_GET(self, request):
        if request.accept == defines.Content_types["application/xml"]:
            self.payload = (defines.Content_types["application/xml"],  "<value>"+str(self.value)+"</value>")
        elif request.accept == defines.Content_types["application/json"]:
            self.payload = (defines.Content_types["application/json"], "{'value': '"+str(self.value)+"'}")
        elif request.accept == defines.Content_types["text/plain"]:
            self.payload = (defines.Content_types["text/plain"], str(self.value))
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    def render_POST(self, request):
        res = self.init_resource(request, MultipleEncodingResource())
        return res


class ETAGResource(Resource):
    def __init__(self, name="ETag"):
        super(ETAGResource, self).__init__(name)
        self.count = 0
        self.payload = "ETag resource"
        self.etag = str(self.count)

    def render_GET(self, request):
        return self

    def render_POST(self, request):
        self.payload = request.payload
        self.count += 1
        self.etag = str(self.count)
        return self

    def render_PUT(self, request):
        self.payload = request.payload
        return self


class AdvancedResource(Resource):
    def __init__(self, name="Advanced"):
        super(AdvancedResource, self).__init__(name)
        self.payload = "Advanced resource"

    def render_GET_advanced(self, request, response):
        response.payload = self.payload
        response.max_age = 20
        response.code = defines.Codes.CONTENT.number
        return self, response

    def render_POST_advanced(self, request, response):
        self.payload = request.payload
        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = "Response changed through POST"
        response.code = defines.Codes.CREATED.number
        return self, response

    def render_PUT_advanced(self, request, response):
        self.payload = request.payload
        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = "Response changed through PUT"
        response.code = defines.Codes.CHANGED.number
        return self, response

    def render_DELETE_advanced(self, request, response):
        response.payload = "Response deleted"
        response.code = defines.Codes.DELETED.number
        return True, response


class AdvancedResourceSeparate(Resource):
    def __init__(self, name="Advanced"):
        super(AdvancedResourceSeparate, self).__init__(name)
        self.payload = "Advanced resource"

    def render_GET_advanced(self, request, response):
        return self, response, self.render_GET_separate

    def render_POST_advanced(self, request, response):
        return self, response, self.render_POST_separate

    def render_PUT_advanced(self, request, response):

        return self, response, self.render_PUT_separate

    def render_DELETE_advanced(self, request, response):
        return self, response, self.render_DELETE_separate

    def render_GET_separate(self, request, response):
        time.sleep(5)
        response.payload = self.payload
        response.max_age = 20
        return self, response

    def render_POST_separate(self, request, response):
        self.payload = request.payload
        response.payload = "Response changed through POST"
        return self, response

    def render_PUT_separate(self, request, response):
        self.payload = request.payload
        response.payload = "Response changed through PUT"
        return self, response

    def render_DELETE_separate(self, request, response):
        response.payload = "Response deleted"
        return True, response

    
#HSMLsensorResource by MiM:

class HSMLsensorResource(Resource):

    def __init__(self, name="HSMLsensorResource", coap_server=None):
        super(HSMLsensorResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

        
        #lst = [22000, 22001, 22002]
        self.add_content_type("application/hsml+json")
        
        print(self.content_type)
        #self.resource_type = "rt1"
        
        self.interface_type = "hsml.collection"
        self.name = "HSMLsensorResource"
        self.path = "/sensors/"
 
        
    def render_GET(self, request):
        #return selected elements from the collection
        #e.g., base element, links, item representations.
        #selection is done in the request
        print("HSML GET:")
        print("request:", request)
        print("request.accept=", request.accept)
        print("request.uri_query=", request.uri_query)
        #TODO: filter response based on accept and uri_query
        #collection IF accept==22000 or if=hsml.collection
        #link IF accept==22001 or if=hsml.link
        #item IF accept==22002 or if=hsml.item
        #?href=sensorname or ?rt=rtype may limit the response
        #NOTE: currently the implementation supports only one uri-query
        #even if multiple parameters can be added to the request
        #by using \& between parameters instead of ?

        rkeys = self._coap_server.root.dump() #resource keys
        hrefoption=None
        rtoption=None
        querys = request.uri_query.split('&')
        for q in querys:
            #if 'href=' in request.uri_query:
            if 'href=' in q:
                hrefoption = q.split('=')[1]
                print("hrefoption=", hrefoption)
            elif 'rt=' in q:
                rtoption = q.split('=')[1]
                print("rtoption=", rtoption)

        if(request.accept == 22000 or 'if=hsml.collection' in request.uri_query): 
        
            #return the whole collection
            
            bi = '[{"bi": "/sensors/"}, {"anchor": "/sensors/", "rel": ["self", "index"]}'
            bi += ', {"href": "/sensors/", "rel": "action", "method": "create", "schema": {"href": "string", "rt": "string", "n": "string", "v": "int"}, "accept": "application/hsml+json", "type": "create"}' #Link extension: action

            bi += ', {"href": "/sensors/", "rel": "action", "method": "create", "schema": {"href": "string", "rt": "string"}, "accept": "application/hsml.link+json", "type": "create"}'

            bi += ', {"href": "/sensors/", "rel": "action", "method": "create", "schema": {"n": "string", "v": "int"}, "accept": "application/hsml.item+json", "type": "create"}'
            
            print(bi)
            #ADD ALL RESOURCES (LINKS+ITEMS)
            ritems=""
            for r in rkeys:
                if "/sensors/" in r:
                    res = self._coap_server.root[r]
                    href = res.name
                    print("href=", href)
                    rt = res.resource_type
                    v = res._payload[0] #"text/plain"
                    print("rt, v: ", rt, v)
                    ritems+=', {"href": "'+href+'", "rt": '+rt+'}'
                    ritems+=', {"n": "'+href+'", "v": '+str(v)+'}'

            print(ritems)
            if ritems=="":
                print("no resources found")
                return self #NOT FOUND
            
            self._payload[22000]=bi+ritems+"]"
            self.actual_content_type = defines.Content_types["application/hsml+json"]
            return self

        elif(request.accept == 22001 or 'if=hsml.link' in request.uri_query): 
            #return only links
            
            bi = '[{"anchor": "/sensors", "rel": ["self", "index"]}'
            print(bi)
            #ADD ALL RESOURCE LINKS
            ritems=""
            for r in rkeys:
                if "/sensors/" in r:
                    res = self._coap_server.root[r]
                    href = res.name
                    print("href=", href)
                    rt = res.resource_type
                    if rtoption is None or rtoption in rt:
                        ritems+=', {"href": "'+href+'", "rt": '+rt+'}'
                    else:
                        print("link did not match with the rt query")

            print(ritems)
            if ritems=="":
                print("no resources found")
                return self #NOT FOUND
            
            self._payload[22001]=bi+ritems+"]"
            self.actual_content_type = defines.Content_types["application/hsml.link+json"]
            return self
        
        elif(request.accept == 22002 or 'if=hsml.item' in request.uri_query): 
            #return only items
            
            bi = '[{"bi": "/sensors"}'
            print(bi)
            #ADD ALL RESOURCE ITEMS
            ritems=""
            for r in rkeys:
                if "/sensors/" in r:
                    res = self._coap_server.root[r]
                    href = res.name
                    print("href=", href)
                    v = res._payload[0] #"text/plain"
                    if hrefoption is None or hrefoption in href:
                        ritems+=', {"n": "'+href+'", "v": '+str(v)+'}'
                    else:
                        print("item did not match with the href query")

            print(ritems)
            if ritems=="":
                print("no resources found")
                return self #NOT FOUND
            
            self._payload[22002]=bi+ritems+"]"
            self.actual_content_type = defines.Content_types["application/hsml.item+json"]
            return self

        else:
            print("GET with ct != 22000-22002") #return NOT ACCEPTABLE
            return self

    def render_PUT(self, request):
        #TODO: update elements by replacing (PATCH for partial update)
        #TODO: Should reply with code CHANGED if success
        #self.edit_resource(request)
        print("HSML PUT")
        ct = request.content_type
        print(ct)
        
        
        if(ct == 22000 or ct == 22001):
            #update ALL links and items in the collection if not selected 
            #using uri-query with href=sensorname
            uriquery = "href" in request.uri_query
            if uriquery:
                #TODO: modify the selected item(s)
                print("href detected: ", request.uri_query)
                href = request.uri_query.split('=')[1] #[0]='href'
                print("href=", href)
                res = self._coap_server.root["/sensors/"+href]
                payload = json.loads(request.payload)[0] #handles only rt, not v if given in payload... TODO!!!!!!!
                print("res.payload in json: ", payload)
                for key, value in payload.items():
                    print("key=", str(key))
                    print("value=", str(value))
                    #set them to the resource:
                    #if str(key) in "rt" or str(key) in "'rt'":
                    if "rt" in str(key):
                        res.resource_type=json.dumps(value)
                        #res.resource_type=value
                        print("new rt: ", res.resource_type)
                    #if str(key) in "'v'":
                    elif "v" in str(key) and ct==22000:
                        #res.payload=json.dumps(value)
                        res.payload=int(value)
                        print("new payload: ", res.payload)
                    else:
                        print("unknown/forbidden parameter: ", str(key))
                
            else:
                print("updating whole collection")
                rkeys = self._coap_server.root.dump()
                payload = json.loads(request.payload)[0]
                print("res.payload in json: ", payload)
                for r in rkeys:
                    if "/sensors/" in r:
                        res = self._coap_server.root[r]
                        href = res.name
                        print("href=", href)
                        for key, value in payload.items():
                            print("key=", key)
                            print("value=", value)
                            #set them to the resource:
                            if key in "rt":
                                res.resource_type=value
                            if key in "v":
                                res.payload=value
                            else:
                                print("unknown/forbidden parameter: ", key)
        elif ct == 22002:
            #the selection is in payload's "n":
            payload = json.loads(request.payload)[0]
            name=str(payload["n"])
            value=int(payload["v"])
            print("name, value=", name, value)
            res = self._coap_server.root["/sensors/"+name]
            res.payload=value
            
            
        else:
            print("wrong content_type: ", ct)
                
        
        return self #should be a CHANGED response code message

    
    def render_POST(self, request):
        #create new elements to collection as defined in request payload
        #res = self.init_resource(request, SensorItemResource())
        #return res

        print("accept=", request.accept)
        print("request.payload", request.payload)
        rpayload = json.loads(request.payload)
        print(type(rpayload)) 
        print("rpayload: ", rpayload)
        ct = request.content_type
        print(ct)
        
        if(request.content_type == 22000): #POST1.txt request file
            #add new item+link as specified in the request payload:
            
            name = str(rpayload[0]["href"])
            print("name=", name)
            newRes=SensorItemResource(name=name, coap_server=self._coap_server)
            newRes.resource_type=rpayload[0]["rt"]
            newRes.content_type=[0, 22001, 22002]
            #newRes.interface_type="application/hsml.item" #TODO: if should be given in request's payload!
            newRes.payload=json.dumps(rpayload[1]["v"]) #only v as text/plain
            self._coap_server.add_resource("sensors/"+name+"/", newRes)

            return(newRes)
        
        if(request.content_type == 22001):
            print("creating new link ", request.payload) #sensor n and v empty
            name = str(rpayload[0]["href"])
            print("name=", name)
            newRes=SensorItemResource(name=name, coap_server=self._coap_server)
            newRes.resource_type=rpayload[0]["rt"]
            #newRes.interface_type="application/hsml.link" #TODO
        
            self._coap_server.add_resource("sensors/"+name+"/", newRes)
            
            return(newRes)
        
        if(request.content_type == 22002):
            print("22002, creating n and v as defined in payload ", request.payload) #automatically create link!
            name = str(rpayload[0]["n"])
            print("name=", name)
            newRes=SensorItemResource(name=name, coap_server=self._coap_server)
            #newRes.resource_type=rpayload[0]["rt"]
            #newRes.interface_type="application/hsml.item"
            newRes.payload=rpayload[0]["v"]
            self._coap_server.add_resource("sensors/"+name+"/", newRes)

            return(newRes)


    #def render_DELETE(self, request):
    def render_DELETE_advanced(self, request, response):
        #remove selected items from collection.
        #if no items selected, remove the whole collection
        if "href" in request.uri_query:
            #delete only the selected item
            print("deleting ", request.uri_query)
            href = request.uri_query.split('=')[1] #[0]='href'
            print("href=", href)
            res = self._coap_server.root["/sensors/"+href]
            res.deleted=True
            print("res name, deleted=", res.name, res.deleted)
            self._coap_server.root.__delitem__("/sensors/"+href)
            return (False, response) 
        elif request.content_type==22000:
            print("deleting the whole collection")
            keys = self._coap_server.root.dump()
            for item in keys:
               
                if item not in "/sensors/" and item is not "/":
                    print(item)
                    res=self._coap_server.root[item]
                    res.deleted=True
                    self._coap_server.root.__delitem__("/sensors/"+res.name)
                    #/sensors itself will be deleted when returning True
            self.deleted=True
            return(True, response)

        else:
            print("ct=22001/2 and no href in uri-query") #METHOD NOT ALLOWED

        return False



        
class SensorItemResource(Resource):
        
    def __init__(self, name="SensorItemResource", coap_server=None):
        super(SensorItemResource, self).__init__(name, coap_server)


    def render_GET(self, request):
        print("SensorItemResource GET")
        return self

    """
    def render_POST(self, request):
        #METHOD NOT ALLOWED
        return self
    """
    
    def render_PUT(self, request):
        self.payload=request.payload
        return self
    
    def render_DELETE(self, request):
        return True
