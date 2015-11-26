from tkinter.ttk import Style

__author__ = 'cheney'
from tkinter import *

class GUIClient(Frame):
    def __init__(self, master=None):
        master.title("My Do-Nothing Application")
        master.minsize(500,500)
        master.maxsize(500,500)
        Frame.__init__(self, master)
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.createWidgets()

    def createWidgets(self):

        self.columnconfigure(1, weight=1)
        self.columnconfigure(4, pad=3)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(10, pad=3)

        userNameText = Label(self, text='User Name:')
        passwordText = Label(self, text='Password: ')
        fileNameText = Label(self, text='File Name:')

        userNameText.grid(sticky=W+N, row=0,column=0, pady=3, padx=3)
        passwordText.grid(sticky=W+N, row=1,column=0, pady=3, padx=3)
        fileNameText.grid(sticky=W+N, row=2,column=0, pady=3, padx=3)

        self.userName = Entry(self)
        self.password = Entry(self)
        self.fileName = Entry(self)

        self.userName.grid(sticky=W+N, row=0,column=1,columnspan=2, pady=3, padx=3)
        self.password.grid(sticky=W+N, row=1,column=1,columnspan=2, pady=3, padx=3)
        self.fileName.grid(sticky=W+N, row=2,column=1,columnspan=2, pady=3, padx=3)

        text = Text(self)
        text.grid(sticky=W+N, row=3,column=0,rowspan=5,columnspan=3)

        registion = Button(self, text='Register')
        removal = Button(self, text='Remove')
        logIn = Button(self, text='Log In')
        logOut = Button(self, text='Log Out')
        download = Button(self, text='Download')

        registion.grid(row=3,column=3, pady=3, padx=3)
        removal.grid(row=4,column=3, pady=3, padx=3)
        logIn.grid(row=5,column=3, pady=3, padx=3)
        logOut.grid(row=6,column=3, pady=3, padx=3)
        download.grid(row=7,column=3, pady=3, padx=3)

        start = Button(self, text='Start')
        exit = Button(self, text='Exit')

        start.grid(sticky=W+N,row=8,column=0, pady=3, padx=3)
        exit.grid(sticky=W+N,row=8,column=1, pady=3, padx=3)

        URLText = Label(self, text='Server URL:')
        URL = Entry(self)

        URLText.grid(sticky=W+N,row=8,column=2, pady=3, padx=3)
        URL.grid(sticky=W+N,row=8,column=3, pady=3, padx=3)



    # def __init__(self, master=None):
    #     Frame.__init__(self, master)
    #     self.pack()
    #
    #     self.entrythingy = Entry()
    #     self.entrythingy.pack()
    #
    #     # here is the application variable
    #     self.contents = StringVar()
    #     # set it to some value
    #     self.contents.set("this is a variable")
    #     # tell the entry widget to watch this variable
    #     self.entrythingy["textvariable"] = self.contents
    #
    #     # and here we get a callback when the user hits return.
    #     # we will have the program print out the value of the
    #     # application variable when the user hits return
    #     self.entrythingy.bind('<Key-Return>',
    #                           self.print_contents)
    #
    # def print_contents(self, event):
    #     print("hi. contents of entry is now ---->",
    #           self.contents.get())
    #
    # def say_hi(self):
    #     print("hi there, everyone!")

root = Tk()
app = GUIClient(master=root)

app.mainloop()