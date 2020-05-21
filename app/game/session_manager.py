class Session_Manager():
    def __init__(self):
        self.current = None
        self.sessionid = 0
    
    def setSession(self, session_obj):
        self.current = session_obj
        self.sessionid += 1

    def endSession(self):
        self.current = None

    def is_active(self):
        if self.current is not None:
            return True
        else:
            return False
    
    def getSession(self):
        return self.current
    
    def getSessionId(self):
        return self.sessionid