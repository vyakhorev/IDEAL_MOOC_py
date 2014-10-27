
class c_Trace():
    """
    The Class Trace provides static methods that can be called from anywhere in the project to record elements of trace.
    A new Event is created by the method startNewEvent(). Events have incremental time codes.
    The other methods add new elements and sub-elements to the current Event.
    """
    def __init__(self, a_tracer):
        self.time = 0
        self.tracer = a_tracer

    def startNewEvent(self):
        if self.tracer is not None:
            self.time += 1
            self.tracer.startNewEvent(self.time)

    def addEventElement(self, ev_name, value = None):
        #if you provide a value (string), it returns None
        if self.tracer is not None:
            if value is not None:
                return self.tracer.addEventElement(ev_name)
            else:
                self.tracer.addEventElement(ev_name, value)

    def addSubelement(self, element, ev_name, textContent = None):
        #if you provide a textContent (string), it returns None
        if self.tracer is not None:
            if textContent is not None:
                return self.tracer.addSubelement(element, ev_name)
            else:
                self.tracer.addSubelement(element, ev_name, textContent)





