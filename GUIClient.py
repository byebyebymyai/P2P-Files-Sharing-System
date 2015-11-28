'''
__author__ = 'byebyebymyai'
'''
from threading import Thread
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
from tkinter.messagebox import showerror
from tkinter import *
from socket import gethostbyname, gethostname
import os

PORT=8080
ADDRESS=gethostbyname(gethostname())
DIRECTORY='./'

LOGIN=False
USERNAME=None
PASSWORD=None
START=False

class GUIClient(Frame):
    def __init__(self, master=None):
        '''
        Constructor of client, used to start the XML-RPC and command line interface.
        '''
        master.title("P2P File Sharing System Client")
        master.minsize(500,510)
        master.maxsize(500,510)
        Frame.__init__(self, master)
        self.pack(fill=BOTH, expand=1)
        self.createWidgets()

    def createWidgets(self):

        self.columnconfigure(1, weight=1)
        self.columnconfigure(1, pad=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(11, pad=1)

        userNameText = Label(self, text='User Name:')
        passwordText = Label(self, text='Password: ')
        fileNameText = Label(self, text='File Name:')

        userNameText.grid(sticky=W+N, row=0,column=0)
        passwordText.grid(sticky=W+N, row=1,column=0)
        fileNameText.grid(sticky=W+N, row=2,column=0)

        self.userName = Entry(self)
        self.password = Entry(self)
        self.fileName = Entry(self)

        self.userName.grid(sticky=W+N+E, row=0,column=1,columnspan=3)
        self.password.grid(sticky=W+N+E, row=1,column=1,columnspan=3)
        self.fileName.grid(sticky=W+N+E, row=2,column=1,columnspan=3)

        self.text = Text(self)
        self.text.grid(sticky=W+N+E, row=3,column=0,rowspan=6,columnspan=3)

        registion = Button(self, text='Register', command=self.register)
        removal = Button(self, text='Remove', command=self.remove)
        logIn = Button(self, text='Log In', command=self.logIn)
        logOut = Button(self, text='Log Out', command=self.logOut)
        download = Button(self, text='Download', command=self.download)
        inquire = Button(self, text='Inquire', command=self.inquire)

        registion.grid(sticky=W+E,row=3,column=3)
        removal.grid(sticky=W+E,row=4,column=3)
        logIn.grid(sticky=W+E,row=5,column=3)
        logOut.grid(sticky=W+E,row=6,column=3)
        download.grid(sticky=W+E,row=7,column=3)
        inquire.grid(sticky=W+E,row=8,column=3)

        start = Button(self, text='Start',command=self.init)
        exit = Button(self, text='Exit',command=self.exit)

        exit.grid(sticky=W+N+E,row=10,column=0)
        start.grid(sticky=W+N+E,row=10,column=1)

        URLText = Label(self, text='Server URL:')
        directoryText = Label(self, text='Directory:')

        URLText.grid(sticky=W+N,row=9,column=2)
        directoryText.grid(sticky=W+N,row=10,column=2)

        self.URL = Entry(self)
        self.directory = Entry(self)

        self.URL.grid(sticky=W+N,row=9,column=3)
        self.directory.grid(sticky=W+N,row=10,column=3)

    def init(self):
        global LOGIN
        global USERNAME
        global PASSWORD
        
        LOGIN=False
        USERNAME=None
        PASSWORD=None
        self._path()

    def _path(self):
        '''
        Input the path of files
        '''
        # Iput the path and check.
        global DIRECTORY
        DIRECTORY=self.directory.get()
        if os.path.exists(DIRECTORY):
            self.text.insert(INSERT,'Input path successfully\n')
            self._connect()
        else:
            self.onDirError()

    def _connect(self):
        '''
        Connect with main server.
        '''
        # Try connect with main server.
        # Check it is a main server or not.
        global START

        main_server_url=self.URL.get()
        try:
            self.main_server_url='http://'+main_server_url
            self.main_server = ServerProxy(self.main_server_url)
            self.main_server.hello()
            self.text.insert(INSERT,'Connect with main server successfully.\n')
            self._start()
            START=True
        except:
            self.onURLError()

    def _start(self):
        s=Server()
        t = Thread(target=s._start)
        t.daemon=True
        t.start()
        self.text.insert(INSERT,'Start P2P client successfully.\n')

    def register(self):
        '''
        Registration by a user on the system.
        '''
        global START

        if START:
            user_name = self.userName.get()
            password = self.password.get()
            if self.main_server.registration(user_name, password):
                self.text.insert(INSERT,'Registration success.\n')
            else:
                self.onAccountError()
        else:
            self.onStartError()

    def remove(self):
        '''
        Removal by a user of themselves from the system.
        '''
        global START

        if START:
            user_name = self.userName.get()
            password = self.password.get()
            if self.main_server.removal(user_name, password):
                self.text.insert(INSERT,'Removal success.\n')
            else:
                self.onAccountError()
        else:
            self.onStartError()
    def logIn(self):
        '''
        Ability by a user to "log in" from the system.
        '''
        global PORT
        global ADDRESS
        global LOGIN
        global USERNAME
        global PASSWORD
        global START

        if START:
            if LOGIN:
                self.onLogInError()
            else:
                user_name = self.userName.get()
                password = self.password.get()
                if self.main_server.logIn(user_name, password, 'http://'+ADDRESS+':'+str(PORT)):
                    LOGIN=True
                    USERNAME=user_name
                    PASSWORD=password
                    self.text.insert(INSERT,'Log in success.\n')
                else:
                    self.onAccountError()
        else:
            self.onStartError()

    def logOut(self):
        '''
        Ability by a user to "log out" from the system.
        '''
        global LOGIN
        global USERNAME
        global PASSWORD
        global START

        if START:
            if LOGIN:
                if self.main_server.logOut(USERNAME, PASSWORD):
                    LOGIN=False
                    USERNAME=None
                    PASSWORD=None
                    self.text.insert(INSERT,'Log out success.\n')
                else:
                    self.onAccountError()
            else:
                self.onLogOutError()
        else:
            self.onStartError()

    def download(self):
        '''
        Used to make the Node find a file and download it.
        '''
        # client_url is the URL of the client which has file.
        global START

        if START:
            if LOGIN:
                file_name=self.fileName.get()
                if file_name == '':
                    self.onFileError()
                else:
                    client_url=self._search(file_name)
                    try :
                        client=ServerProxy(client_url)
                        self._fetch(file_name,client.send(file_name))
                        self.text.insert(INSERT,'Download success.\n')
                    except:
                        self.text.insert(INSERT,'Cannot find file.\n')
            else:
                self.onLogOutError()
        else:
            self.onStartError()

    def exit(self):
        '''
        Exit the client
        '''
        global LOGIN
        global USERNAME
        global PASSWORD
        if LOGIN:
            self.main_server.logOut(USERNAME, PASSWORD)
        self.text.insert(INSERT,'Good bye-bye.')
        sys.exit()

    def inquire(self):
        '''
        Ability by a user to see what files are available to transfer in the local.
        '''
        global START
        if START:
            global DIRECTORY
            files=os.listdir(DIRECTORY)
            for file in files:
                self.text.insert(INSERT,file+'\n')
        else:
            self.onStartError()

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

    def onURLError(self):
        showerror(title='Error',message='Please input URL of server.')

    def onDirError(self):
        showerror(title='Error',message='Please input directory.')

    def onFileError(self):
        showerror(title='Error',message='Please input file.')

    def onAccountError(self):
        showerror(title='Error',message='Please input correct username of password.')

    def onLogInError(self):
        showerror(title='Error',message='Already log in, please logout first.')

    def onLogOutError(self):
        showerror(title='Error',message='Did not log in,please log in first.')

    def onStartError(self):
        showerror(title='Error',message='Please start client.')


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
    root = Tk()
    app = GUIClient(master=root)
    app.mainloop()

if __name__ =='__main__':
    main()
