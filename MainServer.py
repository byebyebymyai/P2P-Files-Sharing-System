'''
@author: cheney
'''
import sqlite3
from xmlrpc.server import SimpleXMLRPCServer

class Server():
    '''
    A centralized server in a peer-to-peer network.
    '''
    def __init__(self):
        '''
        Constructor of main server used to connect with database which save user's information and start server.
        '''
        # Create a new database if server do not have.
        conn = sqlite3.connect('example.db')
        try:
            conn.execute('''CREATE TABLE Users
                            (user_name TEXT PRIMARY KEY, password TEXT NOT NULL, state BOOLEAN NOT NULL, url TEXT NOT NULL, dir TEXT NOT NULL)''')
            print ('Create database and tables successfully')
        except:
            print ('Open database successfully')
        finally:
            conn.close()
        # Start server.
        self._start()
        
    def _start(self):
        '''
        Start the main server
        '''
        # Input a post and check.
        post=input('Input the post of main server:')
        try:
            post=int(post)
        except:
            print('please input a integer as post.')
            self._start()
        
        # Start the server.
        try:
            server = SimpleXMLRPCServer(("localhost",post))
            server.register_instance(self);
            print ('Start the main server successfully')
            server.serve_forever()
        except:
            print('The post already be used, please try again.')
            self._start()
    
    def registration(self):
        '''
        
        '''
    
    def removal(self):
        '''
        
        '''
        
    def logIn(self):
        '''
        
        '''
        
    def logOut(self):
        '''
        
        '''
        
    def searchFile(self):
        '''
        
        '''
    
    def hello(self):
        '''
        Test for network connect
        ''' 
        return "Hello World"        
        
class Client(object):
    
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

    def broadcast(self):
        '''
        
        '''
        
    def search(self):
        '''
        
        '''
    def inquire(self):
        '''
        
        '''
def main():
    '''
    Create a server object.
    '''
    Server()
    
if __name__ =='__main__':
    main()