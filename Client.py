'''
__author__ = 'byebyebymyai'
'''
from cmd import Cmd
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
from socket import gethostbyname, gethostname
import sys
import os


PORT=8080
ADDRESS=gethostbyname(gethostname())
DIRECTORY='./'

LOGIN=False
USERNAME=None
PASSWORD=None

class Client(Cmd):
    '''
    A node in a peer-to-peer network.
    '''
    prompt = '>>'
    def __init__(self):
        '''
        Constructor of client, used to start the XML-RPC and command line interface.
        '''
        Cmd.__init__(self)
        self._path()
        self._connect()
        self._start()
        self.cmdloop()
        # url is the URL of this client.
        # main_server_url is the URL of the centralized server in a peer-to-peer network.
        # directory is the directory where this client save files. 
        # main_server is the centralized server in a peer-to-peer network.

    def _path(self):
        '''
        Input the path of files
        '''
        # Iput the path and check.
        global DIRECTORY
        DIRECTORY=input('Input the path of files which your want to share: ')
        if os.path.exists(DIRECTORY):
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
            print('Cannot connect with sever, please try again.')
            self._connect()

    def _start(self):
        s=Server()
        t = Thread(target=s._start)
        t.daemon=True
        t.start()
        print('Start P2P client successfully.')
            
    def do_register(self,arg):
        '''
        Registration by a user on the system.
        '''
        user_name = input('Input user name: ')
        password = input('Input password: ')
        if self.main_server.registration(user_name, password):
            print('Registration success.')
        else:
            print('The user name is already be used, please try again.')

    def do_remove(self,arg):
        '''
        Removal by a user of themselves from the system.
        '''
        user_name = input('Input user name: ')
        password = input('Input password: ')
        if self.main_server.removal(user_name, password):
            print('Removal success.')
        else:
            print('The user name or password is wrong, please try again.')
    
    def do_logIn(self,arg):
        '''
        Ability by a user to "log in" from the system.
        '''
        global PORT
        global ADDRESS
        global LOGIN
        global USERNAME
        global PASSWORD
        if LOGIN:
            print('Already log in, please logout first.')
        else:
            user_name = input('Input user name: ')
            password = input('Input password: ')
            if self.main_server.logIn(user_name, password, 'http://'+ADDRESS+':'+str(PORT)):
                LOGIN=True
                USERNAME=user_name
                PASSWORD=password
                print('Log in success')
            else:
                print('The user name or password is wrong, please try again.')
        
    def do_logOut(self,arg):
        '''
        Ability by a user to "log out" from the system.
        '''
        global LOGIN
        global USERNAME
        global PASSWORD
        if LOGIN:
            if self.main_server.logOut(USERNAME, PASSWORD):
                LOGIN=False
                USERNAME=None
                PASSWORD=None
                print('Log out success')
            else:
                print('The user name or password is wrong, please try again.')
        else:
            print('Did not log in,please log in first ')
    
    def do_download(self,arg):
        '''
        Used to make the Node find a file and download it.
        '''
        # client_url is the URL of the client which has file.
        if LOGIN:
            file_name=input('Input the file name: ')
            client_url=self._search(file_name)
            try :
                client=ServerProxy(client_url)
                self._fetch(file_name,client.send(file_name))
                print('Download success.')
            except:
                print('Cannot find file')
        else:
            print('Did not log in,please log in first ')

    def do_exit(self,arg):
        '''
        Exit the client
        '''
        global LOGIN
        global USERNAME
        global PASSWORD
        if LOGIN:
            self.main_server.logOut(USERNAME, PASSWORD)
        print('Good bye.')
        sys.exit()

    def do_inquire(self,arg):
        '''
        Ability by a user to see what files are available to transfer in the local.
        '''
        global DIRECTORY
        files=os.listdir(DIRECTORY)
        for file in files:
            print(file)
       
    def _search(self,file_name):
        '''
        Performs a query for a file, possibly asking other known Nodes for
        help.
        '''
        return self.main_server.searchFile(file_name)

    def _fetch(self,file_name,result):
        '''
        Returns the file as a string.
        '''
        global DIRECTORY
        f=open(DIRECTORY+file_name,'w')
        f.write(result)
        f.close()

    def do_hello(self,arg):
        '''
        Test for the connecting with main sever
        '''
        print(self.main_server.hello())

    
class Server():
    '''
    Server part of the node
    '''
    def __init__(self):
        '''
        Constructor
        '''

    def _start(self):
        '''
        Start the server part of client.
        '''
        global PORT
        global ADDRESS
        try:
            server = SimpleXMLRPCServer((ADDRESS, PORT))
            server.register_instance(self)
            server.serve_forever()
        except:
            PORT+=1
            self._start()

    def handle(self,file_name):
        '''
        Used to handle queries.
        '''
        global DIRECTORY
        return os.path.isfile(DIRECTORY+file_name)

    def send(self,file_name):
        global DIRECTORY
        return open(DIRECTORY+file_name).read()

def main():
    '''
    Create a client object.
    '''
    Client()
    
if __name__ =='__main__':
    main()

