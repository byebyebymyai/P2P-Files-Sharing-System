'''
@author: cheney
'''
import sqlite3
from xmlrpc.server import SimpleXMLRPCServer
from socket import gethostbyname, gethostname

class Server():
    '''
    A centralized server in a peer-to-peer network.
    '''
    def __init__(self):
        '''
        Constructor of main server used to connect with database which save user's information and start server.
        '''
        # Create a new database if server do not have.
        self.database='example.db'
        conn = sqlite3.connect(self.database)
        try:
            conn.execute('CREATE TABLE Users (user_name TEXT PRIMARY KEY, password TEXT NOT NULL, state BOOLEAN , url TEXT , dir TEXT )')
            print ('Create database and tables successfully')

        except:
            print ('Open database successfully')
        finally:
            conn.close()
        # Start server.
        self.port = 8000
        self._start()
        
        
    def _start(self):
        '''
        Start the main server
        '''
        # Start the server.
        try:
            server = SimpleXMLRPCServer((gethostbyname(gethostname()),self.port))
            server.register_instance(self)
            print ('Start the main server successfully')
            print("The URL of this server is "+gethostbyname(gethostname())+":"+str(self.port))
            server.serve_forever()
        except:
            self.port+=1
            self._start()
    
    def registration(self, user_name, password, url, dir):
        '''
        Registration by a user on the system
        '''
        conn = sqlite3.connect(self.database)
        try:
            conn.execute('INSERT INTO Users (user_name, password, state, url, dir) VALUES (?, ?, ?, ?, ?)',(user_name, password, True, url, dir))
            conn.commit()
            conn.close()
            return True
        except:
            conn.close()
            return False

    def removal(self,user_name, password):
        '''
        
        '''
        conn = sqlite3.connect(self.database)
        try:
            cursor = conn.execute("SELECT password FROM Users WHERE user_name = ?",(user_name))
            row=cursor.fetchone()
            if row[0] == password:
                conn.execute('DELETE FROM Users WHERE user_name=? ',(user_name))
                conn.commit()
                conn.close()
                return True
            else:
                conn.close()
                return False
        except:
            conn.close()
            return

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