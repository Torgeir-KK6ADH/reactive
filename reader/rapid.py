
import socket
import thread

DEFAULT_TIMEOUT = 10
COMMAND_PORT = 50007
EVENT_PORT = 50008

class ReaderError(Exception):
    """Raised when the reader sends back a status other than 'OK'. 
    """
    
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ConnectionError(Exception):
    """Raised when an error occurrs in the connectivity with the reader. 
    """
    
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Command:
    """Handles connecting to, sending commands to, and parsing 
    the results received from the reader"""
    
    isLive = False
    
    def __init__(self, ipAddress='localhost', timeout=DEFAULT_TIMEOUT):
        """Constructor
        
        Parameters:
            ipAddress - IP Address of the reader
            timeout - Timeout on blocking socket operations
        Exceptions:
            ConnectionError - Errors encountered while setting
            up the Command object
        """
        try:
            self.eventChannels = []
            self.ipAddress = ipAddress
            self.clientSocket = socket.socket()
            self.clientSocket.settimeout(timeout)
        except Exception, e:
            raise ConnectionError, e

    def open(self):
        """Opens the connection to the reader.
        
        Exceptions:
            ConnectionError - Connectivity issue encountered
            while opening the socket
        """
        if not self.isLive:
            try:
                self.clientSocket.connect((self.ipAddress, COMMAND_PORT))
                self.isLive = True;
            except Exception, e:
                raise ConnectionError, e

    def close(self):            
        """Closes the connection to the reader.
        
        Exceptions:
            ConnectionError - Connectivity issue encountered
            while closing the socket
        """
        try:
            while len(self.eventChannels) > 0:
                x = self.eventChannels.pop(0)
                x.close()
        except Exception, e:
            raise ConnectionError, e
        if self.isLive:
            try:
                self.clientSocket.close()
                self.isLive = False
            except Exception, e:
                raise ConnectionError, e
    
    def send(self, command):
        """Send raw C2 commands to the reader.
        
        Parameters:
            command - Complete C2 command to be sent to the reader
        Returns:
            The full non-parsed response from the reader
        Exceptions:
            ConnectionError - Connectivity issue encountered
            while communicating with the reader
        """
        try:        
            self.clientSocket.send(command + "\r\n")
            data = ""
            while 1:
                data = data + self.clientSocket.recv(4096)   
                if (data.find("\r\n\r\n")==-1):
                    continue
                else:
                    break
            return data.strip()
        except Exception, e:
            raise ConnectionError, e
    
    def get(self, config):
        """Returns value of the configuration variable.
        
        Parameters:
            config - C2 variable to get the value for
        Returns:
            The value for the C2 variable
        Exceptions:
            ReaderError - The reader has returned an error
            ConnectionError - Connectivity issue encountered
            while communicating with the reader
        """
        data = self.send(config)
        if data[:2] == 'ok':
            return data[2:].strip()
        else:
            raise ReaderError, data
            
    def set(self, config, value):
        """Sets the value of configuration variable.
        
        Parameters:
            config - C2 variable to be set
            value - New value for the C2 variable
        Exceptions:
            ReaderError - The reader has returned an error
            ConnectionError - Connectivity issue encountered
            while communicating with the reader
        """
        command = config + "=" + value
        data = self.send(command)
        if data[:2] != 'ok':
            raise ReaderError, data
            
    def execute(self, command, *parms):
        """Executes a function call on the reader.
        
        Parameters:
            command - C2 function to be executed on the reader
            parms - Parameters of the function as a tuple
        Returns:
            The full response from the reader with the 'OK'
            removed.
        Exceptions:
            ReaderError - The reader has returned an error
            ConnectionError - Connectivity issue encountered
            while communicating with the reader
        """
        p = str(parms).replace(",)", ")")
        p = p.replace("((", "(")
        p = p.replace("))", ")")
        p = p.replace("\'", "")
        ec = command + p
        data = self.send(ec)
        if data[:2] == 'ok':
            return data[2:].strip()
        else:
            raise ReaderError, data
            
    def getEventChannel(self, function):
        """Creates an event channel and returns the id of the event channel.
        
        Parameters:
            function - Callback function to handle events
        Returns:
            The event channel ID
        """
        e = Event(self.ipAddress)
        self.eventChannels.append(e)
        e.receive(function)
        return e.getid()

class Event:
    """Handles event messages recieved from the reader over a socket connection."""
    def __init__(self, ipAddress='localhost'):
        """Constructor
        
        Parameters:
            ipAddress - IP Address of the reader
        Exceptions:
            ConnenctionError - Error encountered while trying to create
            the event socket
        """
        try:
            self.ipAddress = ipAddress
            self.clientSocket = socket.socket()
            self.clientSocket.connect((self.ipAddress, EVENT_PORT))
            self.id = (self.clientSocket.recv(1024).split('=')[1]).strip()
            self.stop_flag = False
        except Exception, e:
            raise ConnectionError, e
    
    def getid(self):
        """Returns the ID for the event channel.

        Returns:
            The event channel ID
        """
        return self.id
    
    def close(self):
        """Closes the event channel."""
        self.clientSocket.close()
        self.stop_flag = True
        
    def receive(self, function):
        """Starts the receiving thread for events.
        
        Parameters:
            function - Callback function to handle events
        """
        thread.start_new_thread(self.recv_thread, (function,))
        
    def recv_thread(self,function):
        """Thread that continully blocks on the event socket
        waiting for event information. If event information is
        received it is fowarded on to the specified function.
        
        Parameters:
            function - Callback function to handle events
        """
        try:
            data = ""
            while 1:
                while 1:
                    data += self.clientSocket.recv(1024)
                    if self.stop_flag:
                       break;
                    if data.find("\r\n\r\n") == -1:
                        continue
                    else:
                        break
                if self.stop_flag:
                    break;
                index = data.rfind("\r\n\r\n")
                bData = data[:index + 4].strip()
                rc = bData.split("\r\n")
                for x in rc:
                    function(x)
                    if self.stop_flag:
                        break;
                data = data[index + 4:]
                if self.stop_flag:
                    break;
        except:
            pass
    