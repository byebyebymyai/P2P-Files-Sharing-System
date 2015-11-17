'''
@author: cheney
'''
from IN import AF_INET, SOCK_STREAM
from cmd import Cmd
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
from socket import gethostbyname, gethostname
import os

class Server():
    '''
    Server part of the node
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.address=gethostbyname(gethostname())
        self.port=8080
        self._start()

    def _start(self):
        '''
        Start the server part of client.
        '''
        try:
            server = SimpleXMLRPCServer((self.address, self.port))
            server.register_instance(self)
        except:
            self.port+=1
            self._start()
        c=Client('http://'+self.address+str(self.port))
        t = Thread(target=c)
        t.daemon=False
        t.start()
        server.serve_forever()

    def handle(self):
        '''
        Used to handle queries.
        '''
        return 0

class Client(Cmd):
    '''
    A node in a peer-to-peer network.
    '''
    prompt = '>>'
    def __init__(self,url):
        '''
        Constructor of client, used to start the XML-RPC and command line interface.
        '''
        self.url=url
        Cmd.__init__(self)
        self._path()
        self._connect()
        self.cmdloop()
        print('Start P2P client successfully.')
        # url is the URL of this client.
        # main_server_url is the URL of the centralized server in a peer-to-peer network.
        # client_url is the URL of the client which has file.
        # directory is the directory where this client save files. 
        # main_server is the centralized server in a peer-to-peer network.

    def _path(self):
        '''
        Input the path of files
        '''
        # Iput the path and check.
        self.directory=input('Input the path of files which your want to share: ')
        if os.path.exists(self.directory):
            print('Input path successfully')
        else:
            self._path()
            
    def _connect(self):
        '''
        Connect with main server.
        '''
        # Try connect with main server.
        main_server_url=input('Input the URL of main server: ')
        try:
            self.main_server_url='http://'+main_server_url
            self.main_server = ServerProxy(self.main_server_url)
        except:
            print('Cannot connect with this main server,please try again.')
            self._connect()

        # Check it is a main server or not.
        try:
            self.main_server.hello()
            print('Connect with main server successfully.')
        except:
            print('Cannot connect with client, please try again.')
            self._connect()
            
    def do_register(self,arg):
        '''
        Registration by a user on the system.
        '''
        user_name = input("Input user name: ")
        password = input("Input password: ")
        if self.main_server.registration(user_name, password,self.url ,self.directory):
            print("Registration success")
        else:
            print("The user name is already be used, please try again.")

    def do_remove(self,arg):
        '''
        Removal by a user of themselves from the system.
        '''
        user_name = input("Input user name: ")
        password = input("Input password: ")
        if self.main_server.removal(user_name, password):
            print("Removal success")
        else:
            print("The user name or password is wrong, please try again.")
    
    def do_logIn(self,arg):
        '''
        Ability by a user to "log in" from the system.
        '''
        user_name = input("Input user name: ")
        password = input("Input password: ")
        try:
            print(self.main_server.removal(user_name, password, self.directory))
        except:
            print()
        
    def do_logOut(self,arg):
        '''
        Ability by a user to "log out" from the system.
        '''
    
    def do_download(self,arg):
        '''
        Used to make the Node find a file and download it.
        '''
    def do_inquire(self,arg):
        '''
        Ability by a user to see  what files are available to transfer in the local.
        '''
       
    def _search(self):
        '''
        Performs a query for a file, possibly asking other known Nodes for
        help. Returns the file as a string.
        ''' 
        
    def do_hello(self,arg):
        '''
        Test for the connecting with main sever
        '''
        print(self.main_server.hello())

    
    
        
def main():
    '''
    Create a client object.
    '''
    Server()
    
if __name__ =='__main__':
    main()

        